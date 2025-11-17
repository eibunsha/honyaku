from flask import Flask, request, send_file, abort
import os

app = Flask(__name__)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")  # data/spot123/ja.pdf など

SUPPORTED = ["ja", "en", "zh-CN", "zh-TW", "ko", "fr", "de"]

def match_lang(accept_lang: str) -> str:
    """
    Accept-Language ヘッダをもとに最適な言語コードを返す。
    """
    if not accept_lang:
        return "en"

    accept_lang = accept_lang.lower()
    # 例: "ja,en-US;q=0.9" → ["ja", "en-us"]
    langs = [l.split(";")[0].strip() for l in accept_lang.split(",")]

    for lang in langs:
        # 完全一致
        if lang in SUPPORTED:
            return lang

        # ベース言語だけ見る（en-us → en）
        base = lang.split("-")[0]
        if base in SUPPORTED:
            return base

        # 中国語の簡易フォールバック
        if base == "zh":
            return "zh-CN"

    # どれにも当てはまらなければ英語
    return "en"


@app.route("/<spot_id>")
def auto_show(spot_id):
    """
    /spot123 にアクセスされたら、
    Accept-Language を読んで該当言語の PDF をそのまま表示する。
    （ダウンロードダイアログは出さず、ブラウザ内表示）
    """
    accept_lang = request.headers.get("Accept-Language", "")
    lang = match_lang(accept_lang)

    # 言語別PDFのパスを決定
    path = os.path.join(DATA, spot_id, f"{lang}.pdf")
    if not os.path.isfile(path):
        # フォールバック（英語→日本語など）
        fallback_order = ["en", "ja"]
        path = None
        for fb in fallback_order:
            candidate = os.path.join(DATA, spot_id, f"{fb}.pdf")
            if os.path.isfile(candidate):
                path = candidate
                break

        if path is None:
            abort(404, "no file found for this spot")

    # ここがポイント：as_attachment=False で「表示のみ」
    return send_file(path, mimetype="application/pdf", as_attachment=False)


if __name__ == "__main__":
    # ローカル確認用（後でRenderに載せるときも同じ）
    app.run(host="0.0.0.0", port=5000, debug=True)
