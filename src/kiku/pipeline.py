import asyncio

import aiohttp
from loguru import logger

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.services.ollama import OLLamaLLMService
from pipecat.services.openai.stt import OpenAISTTService
from pipecat.services.piper.tts import PiperHttpTTSService
from pipecat.transports.websocket.server import (
    WebsocketServerParams,
    WebsocketServerTransport,
)
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.processors.aggregators.openai_llm_context import (
    OpenAILLMContextFrame,
)

from kiku.config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    PIPER_BASE_URL,
    PIPER_VOICE,
    WHISPER_BASE_URL,
    WHISPER_MODEL,
    WS_HOST,
    WS_PORT,
)
from kiku.prompts import SYSTEM_PROMPT


async def main():
    transport = WebsocketServerTransport(
        params=WebsocketServerParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            add_wav_header=True,
            vad_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
            vad_audio_passthrough=True,
        ),
        host=WS_HOST,
        port=WS_PORT,
    )

    stt = OpenAISTTService(
        api_key="whisper",
        base_url=WHISPER_BASE_URL,
        settings=OpenAISTTService.Settings(
            model=WHISPER_MODEL,
        ),
    )

    llm = OLLamaLLMService(
        base_url=OLLAMA_BASE_URL,
        settings=OLLamaLLMService.Settings(
            model=OLLAMA_MODEL,
        ),
    )

    async with aiohttp.ClientSession() as session:
        tts = PiperHttpTTSService(
            base_url=PIPER_BASE_URL,
            aiohttp_session=session,
            settings=PiperHttpTTSService.Settings(
                voice=PIPER_VOICE,
            ),
        )

        context = OpenAILLMContext(
            messages=[{"role": "system", "content": SYSTEM_PROMPT}],
        )
        context_aggregator = llm.create_context_aggregator(context)

        pipeline = Pipeline(
            [
                transport.input(),
                stt,
                context_aggregator.user(),
                llm,
                tts,
                transport.output(),
                context_aggregator.assistant(),
            ]
        )

        task = PipelineTask(
            pipeline,
            params=PipelineParams(allow_interruptions=True),
        )

        @transport.event_handler("on_client_connected")
        async def on_client_connected(transport, websocket):
            logger.info("Client connected")
            await task.queue_frames([OpenAILLMContextFrame(context=context)])

        @transport.event_handler("on_client_disconnected")
        async def on_client_disconnected(transport, websocket):
            logger.info("Client disconnected")
            await task.queue_frame(asyncio.CancelledError())

        runner = PipelineRunner()
        logger.info(f"Kiku listening on ws://{WS_HOST}:{WS_PORT}")
        await runner.run(task)


if __name__ == "__main__":
    asyncio.run(main())
