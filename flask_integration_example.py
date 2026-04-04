from flask import Flask, request, jsonify, send_file
import tempfile
import os
from marketing_wrapper import (
    run_marketing_audit,
    analyze_competitors,
    get_social_media_plan,
    build_pdf_report
)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "AI Marketing Suite Flask Integration"})

@app.route('/analyze')
def analyze():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        results = run_marketing_audit(url)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/competitor')
def competitor():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        results = analyze_competitors([url])
        return jsonify(results["competitors"][0])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/social-calendar')
def social_calendar():
    topic = request.args.get('topic')
    platforms = request.args.get('platforms', 'linkedin,twitter,instagram').split(',')
    days = int(request.args.get('days', 30))

    if not topic:
        return jsonify({"error": "Topic parameter is required"}), 400

    results = get_social_media_plan(topic, platforms, days)
    return jsonify(results)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        output_path = tmp.name

    try:
        build_pdf_report(data, output_path)
        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='marketing-report.pdf'
        )
    except Exception as e:
        if os.path.exists(output_path):
            os.remove(output_path)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask integration example...")
    app.run(host='0.0.0.0', port=5000, debug=True)
