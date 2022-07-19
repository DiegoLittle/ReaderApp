import { NextApiRequest, NextApiResponse } from 'next';
import {prisma} from '../../lib/prisma';

const { Pool, Client } = require('pg')


// clients will also use environment variables
// for connection information
// const client = new Client()
// await client.connect()
// const res = await client.query('SELECT NOW()')
// await client.end()

export default async (req:NextApiRequest, res:NextApiResponse) => {
    let {q} = req.query
    // console.log(q)
    req.statusCode = 200
    // const text = 'SELECT * FROM papers where arxiv_id is not null ORDER BY date DESC LIMIT 10;'
    const text = 'SELECT * FROM papers where arxiv_id is not null AND num_citations is not null AND title @@ to_tsquery($1) ORDER BY num_citations DESC LIMIT 10;'
    // console.log(text)
    try {
      // pools will use environment variables
  // for connection information
  const client = await new Client({
    user: process.env.PG_USER,
    host: process.env.PG_HOST,
    database: process.env.PG_DATABASE,
    password: process.env.PG_PASSWORD,
    port: process.env.PG_PORT,
  })
  client.connect()
      const db_res = await client.query(text,[q.split(" ").join(" & ")])
      var papers = db_res.rows
      papers.map((item)=>{
        item.categories = JSON.parse(item.categories)
        item.authors = JSON.parse(item.authors)
        item.methods = JSON.parse(item.methods)
        item.tasks = JSON.parse(item.tasks)
        item.refs = JSON.parse(item.refs)
        if(item.num_citations == null && typeof(JSON.parse(item.s2_paper).citationCount) != 'undefined'){
          item.num_citations = JSON.parse(item.s2_paper).citationCount
        }
        return item
      })
      client.end()
      res.json(papers)
      
      // { name: 'brianc', email: 'brian.m.carlson@gmail.com' }
    } catch (err) {
      console.log(err.stack)
    }

}
