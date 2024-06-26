import discord
import logging
import aiohttp
from ...utils import is_url
from .text_handler import TextHandler
from .image_handler import ImageHandler
from .youtube_handler import YoutubeHandler
from .twitter_handler import TwitterHandler
from .generic_url_handler import GenericUrlHandler


class MessageHandler:
    def __init__(
        self, log: logging.Logger, path: str, session: aiohttp.ClientSession
    ) -> None:
        self.log: logging.Logger = log

        self.textHandler: TextHandler = TextHandler(log, path)
        self.imageHandler: ImageHandler = ImageHandler(log, self.textHandler)
        self.ytHandler: YoutubeHandler = YoutubeHandler(log, self.textHandler, session)
        self.twitterHandler: TwitterHandler = TwitterHandler(
            log, self.textHandler, session
        )
        self.genericUrlHandler: GenericUrlHandler = GenericUrlHandler(
            log, self.textHandler, session
        )

    async def isOffending(self, message: discord.Message) -> bool:
        if message.content:
            if self.textHandler.isOffending(message.content):
                return True

            # array of all words, including possible url
            words_of_message = message.content.split()
            for word in words_of_message:
                # check if url is valid
                if not is_url(word):
                    continue

                if "youtu" in word:
                    if await self.ytHandler.isOffending(word):
                        self.log.info(f"Found offending Youtube link: {word}")
                        return True

                elif "twitter" in word:
                    if await self.twitterHandler.isOffending(word):
                        self.log.info(f"Found offending Twitter (x) link: {word}")
                        return True

                # TODO instagram links handler

                else:
                    return await self.genericUrlHandler.isOffending(word)

            return False

        if message.attachments:  # TODO handling gif-ow
            for attachment in message.attachments:
                if not attachment.filename.split(".")[-1] in {
                    "jpeg",
                    "png",
                    "bmp",
                    "tiff",
                }:
                    continue

                if await self.imageHandler.isOffending(await attachment.read()):
                    return True

        return False
