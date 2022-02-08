const cloudflareScraper = require('cloudflare-scraper');

(async () => {
  try {
    const response = await cloudflareScraper.get('https://www.sportsmansguide.com/');
    console.log(response);
  } catch (error) {
    console.log(error);
  }
})();