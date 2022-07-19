import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import { signOut, useSession } from 'next-auth/react'
import { useEffect,useState } from 'react'
import Link from 'next/link'
import EllipsisText from "react-ellipsis-text";

const Home: NextPage = () => {
  const { data: session } = useSession()
  const [bookmarks,setBookmarks] = useState([])
  console.log(session)
  console.log(bookmarks)
  useEffect(async()=>{
  let res = await fetch("/api/bookmarks")
  var data = await res.json()
  console.log(data)
  data = data.reverse()
  setBookmarks(data)
  // setBookmarks([{
  //   title:"test",
  //   url:"https://www.google.com",
  //   description:"test",
  //   type:"web"
  // }])
  },[])
  return (
    <div className="flex flex-col py-2 mx-8 my-8">
      <Head>
        <title>Create Next App</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className=''>
        <h1 className='text-2xl font-semibold'>My bookmarks</h1>
      {bookmarks && bookmarks.map((bookmark)=>
      <Link href={bookmark.url}>
            <div className='text-left w-1/2 my-2  shadow-md hover:bg-blue-50 p-2 rounded-xl cursor-pointer'>
              <div className='text-lg font-semibold inline-flex'>{bookmark.title}</div>
              <div className=''>
              <EllipsisText 
              text={bookmark.description} length={300} />
              </div>
            </div>
            </Link>
            )}
      </div>
      <main className="flex w-full flex-1 flex-col items-center justify-center px-20 text-center">
      
        {/* {session && (

          <div>
            {bookmarks && bookmarks.map((bookmark)=>
            <div>
              <div>{bookmark.title}</div>
            </div>
            )}
            {session.user.email}
            {session.user.image && <Image width={40} height={40} src={session.user.image}></Image>}
          </div>
        )} */}
      </main>

    </div>
  )
}

export default Home


// export async function getServerSideProps(context) {

//   try{
//   let res = await fetch(process.env.NEXT_PUBLIC_API_URL+"api/bookmarks")
//   var bookmarks = await res.json()
// }
// catch{
//   var bookmarks = []
// }
//   return {
//     props: {
//       // csrfToken: await getCsrfToken(context),
//       bookmarks:bookmarks
//     },
//   }
// }