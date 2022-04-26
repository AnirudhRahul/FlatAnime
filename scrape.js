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
    // let res = await needle('get', proxyUrl)
    // if(!res?.body?.data){
    //     console.log("Proxies returned no results rip")
    //     return
    // }
    // for(const item of res.body.data){
    //     ips.push(item.ip+':'+item.port)
    // }
    // console.log(ips)
    // console.log(ips.length)

    // console.log = function(d) {
    //     log_file.write(util.format(d) + '\n');
    // };
      

    const base_search = "https://www.google.com/search?q=anime+minimalist&tbm=isch&ved=2ahUKEwiS4uLYpKn3AhW5hXIEHUKLAOAQ2-cCegQIABAA&oq=anime+minimalist&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgjEO8DECdQ7ilYkS9gzTJoAnAAeACAASyIAaMBkgEBNJgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=WHhjYpLWL7mLytMPwpaCgA4&bih=912&biw=2560&safe=images&hl=en"
    const {body} = await needle('get', base_search)
    const $ = cio.load(body)
    console.log($('a[href]'))


    $('a[href]').each(function(i, elm) {
        // console.log(elm.attribs.href)
        const gurl = elm.attribs.href
        if(gurl.startsWith('/')){
            console.log('https://www.google.com'+gurl)
        }
    });

}

run()
.catch(console.error)