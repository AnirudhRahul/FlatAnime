const needle = require('needle');
const cio = require('cheerio-without-node-native');
const totalWorkers = 100

/**
 * @param {string} url - Genius URL
 */
async function imageQuery(query) {
	const url = ""
    const {body} = await needle('get', url)
    const $ = cio.load(body)

    try {
        // const res = await needle('get', url, {proxyUrl: pickRandom(ips)})
		let { body } = res;
		const $ = cio.load(body);

        

	} catch (e) {
		throw e;
	}
};




const ips = []

function pickRandom(arr){
    return arr[Math.floor(Math.random()*arr.length)]
}

const proxyUrl = `https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=latency&sort_type=asc&protocols=https`

async function run(){
    let res = await needle('get', proxyUrl)
    if(!res?.body?.data){
        console.log("Proxies returned no results rip")
        return
    }
    for(const item of res.body.data){
        ips.push(item.ip+':'+item.port)
    }
    console.log(ips)
    console.log(ips.length)

    console.log = function(d) {
        log_file.write(util.format(d) + '\n');
    };
      
}

run()
.catch(console.error)