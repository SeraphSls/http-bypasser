
const axios = require('axios');
const fs = require('fs');

const HEADERS = {
  'Content-Type': 'application/json',
  'x-algolia-application-id': 'OQUBRX6ZEQ',
  'x-algolia-api-key': '8ad949132d497255ffc04accd141f083',
  'Origin': 'https://remotive.com',
  'Referer': 'https://remotive.com/',
  'User-Agent': 'PostmanRuntime/7.36.3'
};

const ALGOLIA_AGENT_QUERY =
  'x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.2)%3B%20Browser%20(lite)&x-algolia-api-key=8ad949132d497255ffc04accd141f083&x-algolia-application-id=OQUBRX6ZEQ';


const fetchPage = async (page, query = 'python') => {
  const body = {
    requests: [
      {
        indexName: 'live_jobs',
        params: `query=${query}&hitsPerPage=50&page=${page}&facets=["tags","job_type","company_name","locations","category"]`
      }
    ]
  };

  const res = await axios.post(
    'https://oqubrx6zeq-dsn.algolia.net/1/indexes/*/queries',
    body,
    { headers: HEADERS }
  );

  return res.data.results[0].hits;
};

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

const main = async () => {
  const all = [];

  for (let page = 0; page < 5; page++) {
    try {
      const hits = await fetchPage(page, 'python');

      hits.forEach((h) => {
        all.push({
          title: h.title || '',
          company: h.company_name || '',
          location: h.candidate_required_location || '',
          type: h.job_type || '',
          url: h.url || '',
          publication_date: h.publication_date || ''
        });
      });

      console.log(`Page ${page} OK (${hits.length} records)`);
      await delay(700);
    } catch (err) {
      console.error(`Error on page ${page}:`, err.message);
      await delay(1000);
    }
  }

  fs.writeFileSync('../output/jobs_node.json', JSON.stringify(all, null, 2));
  console.log(`File saved with ${all.length} records.`);
};

main();
