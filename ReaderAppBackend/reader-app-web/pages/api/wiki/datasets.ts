import { NextApiRequest, NextApiResponse } from 'next';
import { MongoClient } from 'mongodb'

export default async (req:NextApiRequest, res:NextApiResponse) => {
    // let body = JSON.parse(req.body)
    console.log("Hello World")
    switch (req.method) {
        case 'GET':
            console.log("Hello World")
            const uri =
            "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229";
          const mongo_client = new MongoClient(uri);
            await mongo_client.connect();
            const db = await mongo_client.db("research_papers")
            const collection = await db.collection("entities")
            let entities = await collection.find({"type":"dataset"}).limit(12).toArray()
            await mongo_client.close()
            res.json(entities)
            break;
        default:
            res.setHeader('Allow', [])
            res.status(405).end(`Method ${req.method} Not Allowed`)
        break;
        }
    }
