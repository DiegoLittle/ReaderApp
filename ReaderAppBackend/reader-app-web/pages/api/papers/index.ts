// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
// const { MongoClient } = require("mongodb");
// Replace the uri string with your MongoDB deployment's connection string.
// const uri =process.env.DATABASE_URL
// const client = new MongoClient(uri);
import {prisma} from '../../../lib/prisma'
// const sqlite3 = require('sqlite3').verbose();
// const db = new sqlite3.Database('../dev.db');
const { Pool, Client } = require('pg')

type Data = {
  name: string
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  
  const {skip} = req.query
  if (skip){
    var text = 'SELECT * FROM papers where arxiv_id is not null order by date desc limit 10 offset '+skip

  }
  else{
    var text = 'SELECT * FROM papers where arxiv_id is not null order by date desc limit 10'
  }
    const client = await new Client({
        user: process.env.PG_USER,
        host: process.env.PG_HOST,
        database: process.env.PG_DATABASE,
        password: process.env.PG_PASSWORD,
        port: process.env.PG_PORT,
      })
  try {
    await client.connect();                                 // gets connection
    const { rows } = await client.query(text, []); // sends queries
    // console.log(rows)
    rows.map((item)=>{
      item.categories = JSON.parse(item.categories)
    item.authors = JSON.parse(item.authors)
    item.methods = JSON.parse(item.methods)
    item.tasks = JSON.parse(item.tasks)
    item.refs = JSON.parse(item.refs)
    if(item.s2_paper != null){
    if(item.num_citations == null && typeof(JSON.parse(item.s2_paper).citationCount) != 'undefined'){
      item.num_citations = JSON.parse(item.s2_paper).citationCount
    }
  }
    item.code = JSON.parse(item.code)
    })
    
    res.json(rows)
} catch (error) {
    console.error(error.stack);
} finally {
    await client.end();                                     // closes connection
}


  // finally{
  //   db.close();
  // }
}



// try {
    
//   let papers = await prisma.papers.findMany({
//     where:{
//       NOT:[
//         {
//           arxiv_id:null
//         }
//       ]
//     },
//     orderBy:{
//       date: 'desc'
//     },
//     take:10
//   })
//   papers.map((item)=>{
//     item.categories = JSON.parse(item.categories)
//     item.authors = JSON.parse(item.authors)
//     item.methods = JSON.parse(item.methods)
//     item.tasks = JSON.parse(item.tasks)
//     item.refs = JSON.parse(item.refs)
//     if(item.num_citations == null && typeof(JSON.parse(item.s2_paper).citationCount) != 'undefined'){
//       item.num_citations = JSON.parse(item.s2_paper).citationCount
//     }
//     return item
//   })

//   res.json(papers)
//   // db.all('SELECT * FROM papers', (err, result) => {
//   //   if (err) {
//   //     res.json(err)

//   //     console.error(err.message);
//   //   } else {
//       // result.map((item)=>{
//       //   item.categories = JSON.parse(item.categories)
//       //   item.authors = JSON.parse(item.authors)
//       //   return item
//       // })
//   //     res.json(result)
//   //     // do something with result
//   //   }
//   // })
// } catch (err) {
//   res.status(500).json({ message: err.message })
// }