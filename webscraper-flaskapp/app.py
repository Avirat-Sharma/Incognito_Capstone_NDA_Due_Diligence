from flask import Flask, request, jsonify
from scrapers.webScraperDelaware import delScraper
from scrapers.webScraperUK import uKScraper
from scrapers.webScraperValidator import uKScraper as validatorScraper, delaware_scraper

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Web Scraper API! Use the following endpoints: /delaware_scraper, /uk_scraper, /validate"

@app.route('/delaware_scraper', methods=['GET'])
def delaware_scraper_api():
    """
    API Endpoint to get company details from Delaware website
    URL example: /delaware_scraper?entity_name=Runway
    """
    entity_name = request.args.get('entity_name', type=str)
    if not entity_name:
        return jsonify({'error': 'entity_name parameter is required'}), 400
    
    # Call your delScraper function from Delaware scraper
    df = delScraper(entity_name)
    
    if df is not None:
        return jsonify(df.to_dict(orient="records"))
    else:
        return jsonify({'error': 'No results found'}), 404


@app.route('/uk_scraper', methods=['GET'])
def uk_scraper_api():
    """
    API Endpoint to get company details from the UK Companies House
    URL example: /uk_scraper?entity_name=ION Trading
    """
    entity_name = request.args.get('entity_name', type=str)
    if not entity_name:
        return jsonify({'error': 'entity_name parameter is required'}), 400
    
    # Call your uKScraper function from UK scraper
    df = uKScraper(entity_name)
    
    if isinstance(df, str):  # If no results found, return the string message
        return jsonify({'error': df}), 404
    else:
        return jsonify(df.to_dict(orient="records"))


@app.route('/validate', methods=['GET'])
def validate_scraper_api():
    """
    API Endpoint to validate if company exists in the UK and Delaware
    URL example: /validate?entity_name=ION BOISTEANU PROPERTY TRADING LTD
    """
    entity_name = request.args.get('entity_name', type=str)
    if not entity_name:
        return jsonify({'error': 'entity_name parameter is required'}), 400
    
    # First call the UK scraper and then Delaware scraper
    uk_result = validatorScraper(entity_name)
    
    if uk_result is not None:
        # If exact match is found in the UK scraper, check Delaware
        return jsonify({"status": "Valid", "UK": uk_result.to_dict(orient="records")})
    else:
        delaware_result = delaware_scraper(entity_name)
        if delaware_result:
            return jsonify({"status": "Valid", "Delaware": delaware_result.to_dict(orient="records")})
        else:
            return jsonify({"status": "Invalid", "message": "Company not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
