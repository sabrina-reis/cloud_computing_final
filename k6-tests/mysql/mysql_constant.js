import sql from 'k6/x/sql';
import driver from 'k6/x/sql/driver/mysql';
import {check, sleep}  from 'k6';

const db = sql.open(driver, 'root:infrared-project@tcp(10.128.0.6:3306)/ip_database');

const sampleIPs = JSON.parse(open('./sample_ips.json'));

export let options = {
	stages: [
  	{duration: '5m', target: 25},
	  {duration: '30m', target: 25},
	  {duration: '5m', target: 0},
	],
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
};

export default function () {
  const randomIP = sampleIPs[Math.floor(Math.random() * sampleIPs.length)];
  
  let rows = db.query('SELECT * FROM ip_joined WHERE ip = ? LIMIT 1', randomIP);
  
  check(rows, {
    'query executed': (r) => r !== null,
    'result found': (r) => r.length > 0,
  });
  
}

