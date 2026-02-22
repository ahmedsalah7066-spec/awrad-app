import asyncio
from googletrans import Translator
import sys

async def main():
    translator = Translator()
    text = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ\nقُلْ أَعُوذُ بِرَبِّ النَّاسِ * مَلِكِ النَّاسِ * إِلَهِ النَّاسِ * مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ * الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ * مِنَ الْجِنَّةِ وَالنَّاسِ\n\nTafsir: Surah An-Nas. Say: I seek refuge in the Lord of mankind, the Sovereign of mankind..."
    res = await translator.translate(text, dest='bn')
    print("Original:")
    print(text)
    print("\nTranslated:")
    print(res.text)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
