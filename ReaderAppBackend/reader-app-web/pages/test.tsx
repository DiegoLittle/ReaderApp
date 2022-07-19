import React from 'react'
// import {Popover} from 'react-text-selection-popover'
import css from '@emotion/css'
import dynamic from "next/dynamic";

const Popover = dynamic(() => import('react-text-selection-popover').then((module)=>module.Popover), {
  ssr: false
});
const Test = () => {
  return (
    <div>
      <Popover
  render={
    ({ clientRect, isCollapsed, textContent }) => {
      if (clientRect == null || isCollapsed) return null

      // const style = css`
      //   position: absolute;
      //   left: ${clientRect.left + clientRect.width / 2}px;
      //   top: ${clientRect.top - 40}px;
      //   margin-left: -75px;
      //   width: 150px;
      //   background: blue;
      //   font-size: 0.7em;
      //   pointer-events: none;
      //   text-align: center;
      //   color: white;
      //   border-radius: 3px;
      // `

      return <div className={"absolute w-[150px] bg-blue-500"}>
        Selecting {(textContent || '').length} characters
      </div>
    }
  }
/>
Hello World
    </div>
  )
}

export default Test