import time
import math

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.0) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff if diff > 0 else 0
        elapsed_time = round(diff)
        time_to_completion = round((total - current) / speed) if speed > 0 else 0
        
        progress_str = "[{0}{1}] \nPercent: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 10))]),
            ''.join(["░" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2)
        )
        
        tmp = progress_str + f"{humanbytes(current)} of {humanbytes(total)}\nSpeed: {humanbytes(speed)}/s\nETA: {formatted_time(time_to_completion)}"
        try:
            await message.edit(text=f"{ud_type}\n\n{tmp}")
        except:
            pass

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}B"

def formatted_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = []
    if days: tmp.append(f"{days}d")
    if hours: tmp.append(f"{hours}h")
    if minutes: tmp.append(f"{minutes}m")
    if seconds or not tmp: tmp.append(f"{seconds}s")
    return " ".join(tmp)
