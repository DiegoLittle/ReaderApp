import React from 'react'
// import Annotator from 'react-pdf-ner-annotator';
import dynamic from 'next/dynamic'
// const Annotator = dynamic(() => import('react-pdf-ner-annotator').then((module) => module.Popover), {
//     ssr: false
//   });
  const Annotator = dynamic(() => import('react-pdf-ner-annotator'))

// import the css
// import 'react-pdf-ner-annotator/lib/css/style.css';
// OR import the sass
// import 'react-pdf-ner-annotator/lib/scss/style.scss';

const Page = () => {
  return (
    <div>
        <Annotator url={'https://arxiv.org/pdf/2205.08094.pdf'} />
    </div>
  )
}

export default Page