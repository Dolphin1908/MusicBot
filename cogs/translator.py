import discord # Import thư viện discord
from discord.ext import commands # Import thư viện commands từ discord.ext
from deep_translator import GoogleTranslator # Import Google Translator từ deep_translator
from langdetect import detect # Import hàm detect từ langdetect

class TranslatorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="translate",
                      aliases=["t"],
                      description="Dịch văn bản",
                      usage="!translate <ngôn ngữ đích> <văn bản cần dịch>")
    async def translate(self, ctx, target_lang: str, *, text: str):
        try:
            translated_text = GoogleTranslator(target=target_lang).translate(text)
            await ctx.send(f"🔍 **{target_lang.upper()}**: {translated_text}")
        except Exception as e:
            await ctx.send(f"❌ Lỗi: Không thể dịch. {e}")

    @commands.command(name="detect",
                      description="Phát hiện ngôn ngữ",
                      usage="!detect <văn bản cần phát hiện>")
    async def detect(self, ctx, *, text: str):
        try:
            detected_lang = detect(text)
            await ctx.send(f"🔍 **{detected_lang.upper()}**: {text}")
        except Exception as e:
            await ctx.send(f"❌ Lỗi: Không thể phát hiện ngôn ngữ. {e}")

    @commands.command(name="languages",
                      description="Danh sách ngôn ngữ hỗ trợ",
                      usage="!languages")
    async def languages(self, ctx):
        # Danh sách mã ngôn ngữ (deep_translator không tự động cung cấp)
        lang_codes = {
            "Tiếng Anh": "en", "Tiếng Việt": "vi", "Tiếng Nhật": "ja", "Tiếng Hàn": "ko",
            "Tiếng Pháp": "fr", "Tiếng Đức": "de", "Tiếng Trung (Giản thể)": "zh-cn", 
            "Tiếng Trung (Phồn thể)": "zh-tw", "Tiếng Tây Ban Nha": "es", "Tiếng Ý": "it"
        }

        # Ghép tên ngôn ngữ với mã tương ứng
        languages_list = "\n".join(f"🔹 **{lang}**: {code}" for lang, code in lang_codes.items())

        await ctx.send(f"🌐 **Ngôn ngữ hỗ trợ:**\n{languages_list}")
        
async def setup(bot):
    await bot.add_cog(TranslatorCog(bot))
