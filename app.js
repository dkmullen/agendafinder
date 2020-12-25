const url = 'https://destinyhosted.com/agenda_publish.cfm?id=56691';
const puppeteer = require('puppeteer');
const $ = require('cheerio');

const scraper = (url, tagString) => {
  return puppeteer
  .launch()
  .then(browser => {
    return browser.newPage();
  })
  .then(page => {
    return page.goto(url).then(() => {
      return page.content();
    });
  })
  .then(html => {
    let results = [];
    $(tagString, html).each(function() {
      results.push($(this).html());
    });
    return results;
  })
  .catch((err) => {
    console.log(err);
  });
}

scraper(url, '#list tbody > tr > td')
  .then(results => {
    let parsedResults = [];
    let i = 0;
    while (i < results.length) {
      let parsedLink = results[i].trim();
      let fullLink = `${parsedLink.slice(0, 9)}https://destinyhosted.com/${parsedLink.slice(9)}`;
      parsedResults.push({ link: fullLink, name: results[i + 1].trim().replace(/<\/?[^>]+(>|$)/g, '') });
      i += 4;
    }
    console.log(parsedResults);
    process.exit();
  })
  .catch(err => {
    console.log(err);
  });

  /*
  Each table row contains four tds (called 'results'). The first contains the date wrapped in the link. 
  The second contains the name of the meeting. The function above strips out spaces for the first two results;
  Then it adds in the destinyhosted part of the address, then creates an object with
  the link and the meeting name as key/value; then it skips ahead over two empty cells to the next link.
  */