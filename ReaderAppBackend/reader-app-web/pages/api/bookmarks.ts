import { NextApiRequest, NextApiResponse } from 'next';
import { getSession } from 'next-auth/react';
import {prisma} from '../../lib/prisma';
export default async (req:NextApiRequest, res:NextApiResponse) => {
    console.log("Getting session")

    const session = await getSession({ req })
    console.log("Debug")
    if(session){
    let user = await prisma.user.findFirst({
        where:{
            email: session.user.email
        }
    })
    console.log(user)
    let bookmarks = await prisma.bookmarks.findMany({
        where:{
            owner_id: user.id
        }
    })
    console.log(bookmarks)
    res.json(bookmarks)
}
else{
    res.json([])
}


    req.statusCode = 200

}