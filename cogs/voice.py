import discord # Import thư viện discord
from discord.ext import commands # Import thư viện commands từ discord.ext
import yt_dlp as youtube_dl # Import yt_dlp để tải thông tin video từ Youtube
import asyncio # Import asyncio để sử dụng coroutine
from collections import deque # Import deque để sử dụng hàng đợi
from utils.supporter import format_duration # Import hàm format_duration từ file supporter.py

# Cài đặt cho youtube_dl
YDL_OPTS = {
    'format': 'bestaudio/best', # Chọn format audio tốt nhất
    'postprocessors': [{ # Chọn postprocessor để xử lý audio
        'key': 'FFmpegExtractAudio', # Chọn FFmpeg để extract audio
        'preferredcodec': 'mp3', # Chọn codec mp3
        'preferredquality': '192', # Chọn chất lượng 192kbps
    }],
    'noplaylist': True, # Không phát danh sách phát
    'quiet': True # Không hiển thị log
}

# Cài đặt cho ffmpeg
FFMPEG_OPTS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', # Reconnect khi bị disconnect
    'options': '-vn' # Chỉ lấy audio
}

SEARCH_OPTS = {
        'format': 'bestaudio/best', 
        'noplaylist': True,
        'quiet': True,
        'extract_flat': False,  # Không tải xuống video, chỉ lấy thông tin
        'default_search': 'ytsearch',  # Tìm kiếm trên YouTube
    }

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # Lưu lại bot để sử dụng trong các hàm khác
        self.music_queue = deque() # Hàng đợi nhạc
        self.current_song = None # Bài hát đang phát
        self.voice_check_task = self.bot.loop.create_task(self.check_voice_state()) # Task kiểm tra voice state

    @commands.command(name="join",
                      description="Tham gia voice channel",
                      usage="!join")
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("Bạn đang không ở trong voice channel nào.")
    
    @commands.command(name="leave",
                      description="Rời khỏi voice channel",
                      usage="!leave")
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Bot không ở trong voice channel nào.")

    @commands.command(name="play",
                      aliases=["p"],
                      description="Phát nhạc từ Youtube",
                      usage="!play <url>")
    async def play(self, ctx, *, query: str, from_queue=False):
        if not ctx.voice_client:
            await ctx.invoke(self.join) # Gọi lệnh join nếu bot chưa ở trong voice channel
        
        voice_client = ctx.voice_client # Lấy voice client

        if not from_queue: # Nếu không phải từ hàng đợi thì tìm kiếm bài hát
            is_url = query.startswith("http") # Kiểm tra xem query có phải là url không
            if not is_url: # Nếu không phải url thì tìm kiếm trên Youtube
                try:
                    with youtube_dl.YoutubeDL(SEARCH_OPTS) as ydl:
                        info = ydl.extract_info(f"ytsearch5:{query}", download=False)
                        if not info or 'entries' not in info:
                            await ctx.send("❌ Không tìm thấy bài hát nào.")
                            return

                        results = info['entries'][:5]
                        search_results = [
                            f"{i+1}. **{entry.get('title', 'Không xác định')}** - `{format_duration(entry.get('duration', 'Không xác định'))}`"
                            for i, entry in enumerate(results)
                        ]

                        message = await ctx.send(
                            "🔎 **Kết quả tìm kiếm:**\n" + "\n".join(search_results) + 
                            "\n\n📌 **Nhấn vào số (1-5) hoặc nhập số để chọn bài hát.**"
                        )

                        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                        for emoji in emojis:
                            await message.add_reaction(emoji)

                        def check(reaction, user):
                            return user == ctx.author and str(reaction.emoji) in emojis and reaction.message.id == message.id

                        try:
                            reaction, _ = await self.bot.wait_for("reaction_add", timeout=20.0, check=check)
                            choice = emojis.index(str(reaction.emoji))  # Chuyển emoji thành index
                        except asyncio.TimeoutError:
                            await ctx.send("⏳ Hết thời gian chọn bài hát.")
                            return

                        selected_song = results[choice]
                        url = selected_song['url']  # Cập nhật query thành URL bài hát đã chọn
                        title = selected_song.get('title', 'Không xác định')
                        duration = format_duration(selected_song.get('duration', 'Không xác định'))

                except youtube_dl.utils.DownloadError as e:
                    await ctx.send("❌ Lỗi khi tìm kiếm bài hát. Vui lòng thử lại.")
                    print(f"Lỗi khi tìm kiếm bài hát: {e}")
                    return
                #try:
                #    with youtube_dl.YoutubeDL(SEARCH_OPTS) as ydl: # Sử dụng youtube_dl để tìm kiếm trên Youtube
                #        info = ydl.extract_info(query, download=False) # Lấy thông tin video
                #        if 'entries' in info: # Kiểm tra xem có kết quả tìm kiếm không
                #            url2 = info['entries'][0]['url']  # Lấy url của video
                #            title = info['entries'][0].get('title', 'Không xác định') # Lấy title của video
                #            duration = format_duration(info['entries'][0].get('duration', 'Không xác định')) # Lấy duration của video
                #        else: # Nếu không có kết quả tìm kiếm
                #            await ctx.send("❌ Không tìm thấy bài hát nào.")
                #            return
                #except youtube_dl.utils.DownloadError as e: # Bắt lỗi nếu không tìm thấy thông tin video
                #    await ctx.send("❌ Lỗi không tìm thấy thông tin bài hát. Vui lòng thử lại.")
                #    print(f"Lỗi không tìm thấy thông tin bài hát: {e}")
                #    return

            else: # Nếu là url thì lấy thông tin video
                try:
                    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl: # Sử dụng youtube_dl để lấy thông tin video
                        info = ydl.extract_info(query, download=False) # Lấy thông tin video
                        url = info['url'] # Lấy url của video
                        title = info.get('title', 'Không xác định') # Lấy title của video
                        duration = format_duration(info.get('duration', 'Không xác định')) # Lấy duration của video
                except youtube_dl.utils.DownloadError as e: # Bắt lỗi nếu không lấy được thông tin video
                    await ctx.send("❌ Lỗi khi lấy thông tin bài hát. Vui lòng thử lại.")
                    print(f"Lỗi khi lấy thông tin bài hát: {e}")
                    return

            song_info = {
                "url": url,  # URL stream
                "title": title, # Tiêu đề
                "duration": duration # Thời lượng
            }
            # Nếu đang phát nhạc thì thêm vào hàng đợi
            if voice_client.is_playing():
                await ctx.send(f"➕ Đã thêm **{title}** - `{duration}` vào hàng đợi!")
                self.music_queue.append(song_info)
                return

        else: # Nếu từ hàng đợi thì lấy thông tin từ query
            url = query['url'] # Lấy url từ query
            title = query.get('title', 'Không xác định') # Lấy title từ query
            duration = query.get('duration', 'Không xác định') # Lấy duration từ query

        # Chuyển đổi url thành source để phát nhạc
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url, **FFMPEG_OPTS), volume=0.5)

        ''' Hàm sau sẽ được gọi khi bài hát kết thúc '''
        def after_play(error):
            if error: # Kiểm tra lỗi
                print(f"Lỗi phát nhạc: {error}")
            # Kiểm tra và gọi phát bài tiếp theo
            future = asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)
            try:
                future.result()  # Để bắt lỗi nếu có
            except Exception as e:
                print(f"Lỗi khi gọi play_next: {e}")

        # Phát nhạc
        voice_client.play(source, after=after_play)

        # Gửi thông báo
        await ctx.send(f"🎵 Đang phát: **{title}** - `{duration}`")

    async def play_next(self, ctx):
        """Phát bài tiếp theo trong hàng đợi"""
        if self.music_queue:
            next_song = self.music_queue.popleft() # Lấy bài hát đầu tiên trong hàng đợi
            await ctx.invoke(self.play, query=next_song, from_queue=True) # Gọi lệnh play để phát bài hát
        else:
            await asyncio.sleep(300)  # Chờ 30 giây trước khi rời kênh
            if ctx.voice_client and not ctx.voice_client.is_playing(): # Kiểm tra xem có đang phát nhạc không
                await ctx.voice_client.disconnect() # Rời kênh voice
                await ctx.send("🔇 Không còn nhạc, bot rời kênh voice.")

    @commands.command(name="queue", 
                      aliases=["q"], 
                      description="Hiển thị danh sách nhạc đang chờ", 
                      usage="!queue")
    async def queue(self, ctx):
        """Hiển thị danh sách nhạc đang chờ"""
        if not self.music_queue:
            await ctx.send("📭 Hàng đợi trống.")
        else:
            queue_list = "\n".join(f"{i+1}. {url}" for i, url in enumerate(self.music_queue))
            await ctx.send(f"📜 **Danh sách phát:**\n{queue_list}")

    @commands.command(name="pause",
                      description="Tạm dừng phát nhạc",
                      usage="!pause")
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Đã tạm dừng.")
        else:
            await ctx.send("Không có bài hát nào đang phát.")
    
    @commands.command(name="resume",
                      description="Tiếp tục phát nhạc",
                      usage="!resume")
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Tiếp tục phát.")
        else:
            await ctx.send("Không có bài hát nào đang tạm dừng.")

    @commands.command(name="stop",
                      description="Dừng phát nhạc",
                      usage="!stop")
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏹️ Đã dừng phát.")
        else:
            await ctx.send("Không có bài hát nào đang phát.")

    @commands.command(name="skip",
                      description="Bỏ qua bài hát hiện tại",
                      usage="!skip")
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop() # Dừng bài hát hiện tại
            ctx.voice_client.resume() # Tiếp tục phát bài tiếp theo
            await ctx.send("⏭️ Đã bỏ qua bài hát.")
        else:
            await ctx.send("Không có bài hát nào đang phát")

    @commands.command(name="clearqueue",
                      aliases=["clearq"],
                      description="Xóa hết hàng đợi",
                      usage="!clearqueue")
    async def clear_queue(self, ctx):
        self.music_queue.clear()
        await ctx.send("🗑️ Đã xóa hết hàng đợi.")

    @commands.command(name="nowplaying",
                      aliases=["np"],
                      description="Hiển thị bài hát đang phát",
                      usage="!nowplaying")
    async def now_playing(self, ctx):
        if ctx.voice_client.is_playing():
            title = self.current_song.get('title', 'Không xác định')
            duration = format_duration(self.current_song.get('duration', 'Không xác định'))
            await ctx.send(f"🎵 **{title}** - `{duration}`")
        else:
            await ctx.send("Không có bài hát nào đang phát.")

    @commands.command(name="volume",
                      description="Điều chỉnh âm lượng",
                      usage="!volume <số>")
    async def volume(self, ctx, volume: int):
        if ctx.voice_client:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"🔊 Đã điều chỉnh âm lượng thành {volume}%")
        else:
            await ctx.send("Bot không ở trong voice channel nào.")
    
    async def check_voice_state(self):
        """Kiểm tra bot có bị disconnect không và kết nối lại nếu cần"""
        while True:
            await asyncio.sleep(300)  # Cứ 30s kiểm tra một lần
            for vc in self.bot.voice_clients:
                if not vc.is_playing() and not vc.is_paused() and not self.music_queue:
                    await vc.disconnect()

async def setup(bot):
    await bot.add_cog(VoiceCog(bot)) # Thêm cog vào bot