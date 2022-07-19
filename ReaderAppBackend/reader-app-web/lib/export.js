const { Pool, Client } = require('pg')
var fs = require('fs')


async function main(){
    const client = await new Client({
        user: "diego",
        host: "165.232.156.229",
        database: "research_papers",
        password: "83o2Zw5GKzMQiH923u2OzKBHCZNUw",
        port: 5432,
      })
      const copyTo = require('pg-copy-streams').to
      
      await client.connect()
      const q = `COPY papers to STDOUT with csv DELIMITER ';'`
      const dataStream = client.query(copyTo(q))
      dataStream.pipe(fs.createWriteStream('papers.csv'))
      dataStream.on('error', async function (err) {
        // Here we can controll stream errors
        await client.end()
      })
      dataStream.on('end', async function () {
        await client.end()
      })
}

main()

