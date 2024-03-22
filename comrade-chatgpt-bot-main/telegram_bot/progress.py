async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not await is_user_allowed(user.id):
        logger.info(f"User {user.id} ({user.username}) tried to generate an image but is not allowed.")
        await update.message.reply_text("Sorry, you are not allowed to generate images.")
        return

    """Generate an image based on a prompt and send it back to the user as an image."""
    if not context.args:
        logger.error(f"User {user.id} ({user.username}) did not provide a prompt for the /image command.")
        await update.message.reply_text("Please provide a description for the image after the /image command.")
        return

    prompt = ' '.join(context.args)
    logging.info(f"User {user.id} ({user.username}) requested an image with prompt: '{prompt}'")

    # This function will be used to keep sending the typing action
    async def keep_typing():
        while keep_typing.is_typing:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')# при обновлении чата мы будем  транслировать пользователю upload photo
            await asyncio.sleep(5)

    keep_typing.is_typing = True

    typing_task = asyncio.create_task(keep_typing()) #запускаем анимацию набора текста

    try:
        response = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="b64_json"
            )
        )

        keep_typing.is_typing = False
        await typing_task

        if hasattr(response, 'data') and len(response.data) > 0:
            await update.message.reply_photo(photo=BytesIO(base64.b64decode(response.data[0].b64_json)))
            logging.info(f"Successfully generated an image for prompt: '{prompt}'")
        else:
            await update.message.reply_text("Sorry, the image generation did not succeed.")
            logging.error(f"Failed to generate image for prompt: '{prompt}'")

    except Exception as e:
        keep_typing.is_typing = False
        await typing_task

        logging.error(f"Error generating image for prompt: '{prompt}': {e}")
        await update.message.reply_text("Sorry, there was an error generating your image.")
