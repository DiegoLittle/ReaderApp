import { NextApiRequest, NextApiResponse } from 'next';
import { MongoClient } from 'mongodb';
const uri =
"mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229";
const mongo_client = new MongoClient(uri);

await mongo_client.connect();
const database = await mongo_client.db('research_papers');
const pages = await database.collection('pages');

interface Page{
    title: string;
    slug: string;
    resource_name: string;
    aliases: string[];
    description: string
    related_papers: []
    datasets: []
    related_concepts: string[]
    tags: string[]
    type: string
}
interface PageFetch{
    error:boolean
}


export default async (req:NextApiRequest, res:NextApiResponse) => {
    // let body = JSON.parse(req.body)
    // console.log(req)
    switch (req.method) {
        case 'GET':
            var {title} = req.query
            let wiki_req = await fetch("http://localhost:8000/api/wiki?q="+title)
            let wiki = await wiki_req.json()
            console.log(wiki)
            res.json(wiki)
           
            break;
        case 'POST':
            let page = JSON.parse(req.body)
            let insert_result = await pages.insertOne(page)
            res.json(insert_result)
            break;
        default:
            res.setHeader('Allow', [])
            res.status(405).end(`Method ${req.method} Not Allowed`)
        break;
        }
    }
