import { NextApiRequest, NextApiResponse } from 'next';
import { MongoClient } from 'mongodb'
const { Pool, Client } = require('pg')


export default async (req:NextApiRequest, res:NextApiResponse) => {

    let annotation = JSON.parse(req.body)
    const uri =
    "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229";
  const mongo_client = new MongoClient(uri);
    await mongo_client.connect();
    const database = await mongo_client.db('research_papers');
    const entities = await database.collection('entities');
    annotation.inserted_at = new Date()
    var insert_res = await entities.insertOne(annotation)
    console.log(annotation.name)
    console.log(annotation.sources[0])
    let arxiv_id = annotation.sources[0].split("pdf/")[annotation.sources[0].split("pdf/").length-1].replace(".pdf","")
    var link= {
      span: annotation.name,
      link: {
        name: annotation.name,
        type: annotation.type,
        source: annotation.sources[0],
    }
  }
    let body = {
      arxiv_id: arxiv_id,
      link: link
    }
    let add_request = await fetch("http://localhost:8000/api/papers/entity_link",{
      method: "POST",
      body: JSON.stringify(body),
    })
    let add_res = await add_request.json()
    console.log(add_res.message)

    


    // Should signal to update the entity links for the paper
    // interface link {
    //   span: string
    //   link: {
    //     name: string
    //     type: string
    //     source: string
    //   }
    //   pages: number[]
    // }
    res.status(200).json(insert_res)

}