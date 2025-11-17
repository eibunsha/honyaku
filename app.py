from flask import Flask, request, send_file, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAI クライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 対応言語
LANG_MAP = {
    "ja": "ja",
    "en": "en",
    "zh": "zh",
    "ko": "ko",
    "fr": "fr"
}

# 各国語テキスト（宮ヶ瀬ダム）
TEXT = {
    "ja": "宮ヶ瀬ダムは神奈川県清川村に位置する大規模な観光スポットです。四季折々の自然美が楽しめ、特に紅葉の季節には多くの観光客が訪れます。大噴水やイルミネーションイベントも人気で、家族連れにもおすすめです。",
    "en": "Miyagase Dam is a major tourist attraction located in Kiyokawa Village, Kanagawa Prefecture. Visitors can enjoy beautiful nature in every season, especially the autumn leaves. The large fountain and winter illumination events are also very popular.",
    "zh": "宫ヶ濑大坝位于神奈川县清川村，是著名的观光景点。四季都有不同的自然美景，尤其是红叶季节最具魅力。大型喷泉和冬季灯饰活动也深受游客喜爱。",
    "ko": "미야가세 댐은 가나가와현 키요카와촌에 위치한 유명 관광지입니다. 사계절 내내 아름다운 풍경을 즐길 수 있으며, 특히 단풍철에 많은 관광객이 찾습니다. 대형 분수와 일루미네이션 행사도 인기입니다.",
    "fr": "Le barrage de Miyagase est une attraction touristique majeure située dans le village de Kiyokawa, préfecture de Kanagawa. On peut y profiter de magnifiques paysages naturels toute l'année, notamment en automne. La grande fontaine et les illuminations saisonnières sont également très populaires."
}

def detect_language():
    lang = request.headers.get("Accept-Language", "ja")
    lang = lang[:2].lower()
    return LANG_MAP.get(lang, "ja")

# 音声を直接返すエンドポイント
@app.route("/spot_miyagase_tts")
def spot_miyagase_tts():
    lang = detect_language()
    text = TEXT[lang]

    speech_file = "voice_output.mp3"

    # 最新の高品質音声API
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text
    ) as resp:
        resp.stream_to_file(speech_file)

    return send_file(speech_file, mimetype="audio/mpeg")

# HTML プレイヤーつきページ
@app.route("/spot_miyagase_voice")
def spot_miyagase_voice():
    lang = detect_language()
    text = TEXT[lang]

    html = f"""
    <html>
    <body>
        <h1>宮ヶ瀬ダム 音声ガイド（{lang}）</h1>
        <audio controls autoplay>
            <source src="/spot_miyagase_tts" type="audio/mpeg">
        </audio>
        <p>{text}</p>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/")
def home():
    return "音声ガイドサーバー稼働中 /spot_miyagase_tts /spot_miyagase_voice"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
