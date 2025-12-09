

import xk6_mongo from 'k6/x/mongo';
import {check, sleep} from 'k6';

const client = xk6_mongo.newClient('mongodb://10.128.0.7:27017');

// Load real IPs from sample file
const sampleIPs = JSON.parse(open('../sample_ips.json'));

export let options = {
	stages: [
		{duration: '10m', target: 10},
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],	
  ],
};

export default async function () {
  const randomIP = sampleIPs[Math.floor(Math.random() * sampleIPs.length)];
  
  const doc = await client.findOne('ip_database', 'ip_metadata', { ip: randomIP });
  
  check(doc, {
    'query executed': (d) => true,
    'document found': (d) => d !== null,
  });
  
}

