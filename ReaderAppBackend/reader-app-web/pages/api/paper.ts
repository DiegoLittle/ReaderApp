import { NextApiRequest, NextApiResponse } from 'next';
const { Pool, Client } = require('pg')

export default async (req:NextApiRequest, res:NextApiResponse) => {
    let {arxiv_id} = req.query
    const text = 'SELECT * FROM papers where arxiv_id = $1'
    const client = await new Client({
        user: process.env.PG_USER,
        host: process.env.PG_HOST,
        database: process.env.PG_DATABASE,
        password: process.env.PG_PASSWORD,
        port: process.env.PG_PORT,
      })
    try {
        await client.connect();                                 // gets connection
        const { rows } = await client.query(text, [arxiv_id]); // sends queries
        var item = rows[0]
        if(typeof(item) != 'undefined'){
        item.categories = JSON.parse(item.categories)
        item.authors = JSON.parse(item.authors)
        item.methods = JSON.parse(item.methods)
        item.tasks = JSON.parse(item.tasks)
        item.refs = JSON.parse(item.refs)
        if(item.num_citations == null && typeof(JSON.parse(item.s2_paper).citationCount) != 'undefined'){
          item.num_citations = JSON.parse(item.s2_paper).citationCount
        }
        item.code = JSON.parse(item.code)
        console.log(item.code)
        res.json(item)
    }
    else{
        res.json({error:"No document found"})
    }
    } catch (error) {
        console.error(error.stack);
    } finally {
        await client.end();                                     // closes connection
    }
    // res.json(rows)

}