const CloudflareBypasser = require('cloudflare-bypasser');

let cf = new CloudflareBypasser();

cf.request('https://linktracker.pro')
.then(res => {
    // console.log(res);
  // res - full response
});

cf.request({
  url: 'https://www.sportsmansguide.com/',
  headers: {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  },
  options: {
    resolveWithFullResponse: true,
    simple                 : false,
    followRedirect         : false
  }
})
.then(res => {
    console.log(res);
  // res - full response
}, (err) => {
    console.log(`error: ${err}`)
})