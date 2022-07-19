import { MongoClient } from 'mongodb'

const uri =
      "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229";
export const mongo_client = new MongoClient(uri);


export async function fetch_dataset(title){
    const uri =
    "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229";
  const mongo_client = new MongoClient(uri);
    await mongo_client.connect();
    const database = await mongo_client.db('research_papers');
    const methods = await database.collection('datasets');
    var results = await methods.findOne({
      "full_name": title
    })
    results = await results
    return results
  }

export async function fetch_method(title){
  const uri =
  "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229";
const mongo_client = new MongoClient(uri);
  await mongo_client.connect();
  const database = await mongo_client.db('research_papers');
  const methods = await database.collection('methods');
  var results = await methods.find({
    "name": title
  })
  results = await results.toArray()
  return results
}
