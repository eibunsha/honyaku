from flask import Flask, render_template, send_file, abort

app = Flask(__name__)

# 言語コード → PDFファイル名の対応表
LANG_MAP = {
    "ja": "ja.pdf",
    "en": "en.pdf",
    "fr": "fr.pdf",
    "ko": "ko.pdf",
    "zh-cn": "zh-CN.pdf",  # 中国語（簡体）
    "zh-cn": "zh-CN.pdf",
    "zh": "zh-CN.pdf",
}


def normalize_lang(lang: str) -> str:
    """
    URLで受け取った lang を正規化する
    例: fr-FR → fr / zh-TW → zh-cn など
    """
    if not lang:
        return "ja"

    lang = lang.lower()

    # 完全一致
    if lang in LANG_MAP:
        return lang

    # fr-FR → fr, en-US → en
    base = lang.split("-")[0]
    if base in LANG_MAP:
        return base

    # 中国語はとりあえず zh-cn に寄せる
    if base == "zh":
        return "zh-cn"

    # それ以外は日本語にフォールバック
    return "ja"


@app.route("/spot_miyagase")
def spot_miyagase_page():
    """
    メインのページ。
    HTML（音声ボタン＋PDF表示）を返す。
    """
    return render_template("spot_miyagase.html")


@app.route("/spot_miyagase/pdf/<lang>")
def spot_miyagase_pdf(lang):
    """
    指定された lang のPDFを返す。
    例: /spot_miyagase/pdf/ja, /spot_miyagase/pdf/en
    """
    norm = normalize_lang(lang)
    filename = LANG_MAP.get(norm, LANG_MAP["ja"])
    path = f"data/spot_miyagase/{filename}"

    try:
        return send_file(path)
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    # ローカル実行用（Renderでは無視されます）
    app.run(host="0.0.0.0", port=10000)
