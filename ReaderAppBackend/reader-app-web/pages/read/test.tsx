import React from 'react'
import { MathJax } from 'better-react-mathjax'
const Test = () => {
  return (
    <div>
        <p>
               {/* This is text which involves math <MathJax><math mode='display' xmlns='http://www.w3.org/1998/Math/MathML'><mrow><msub><mover accent='true'><mi>s</mi> <mo>&#x2DC;</mo></mover> <mrow><mi>l</mi><mi>i</mi></mrow> </msub><mrow><mo>(</mo><mi>q</mi><mo>,</mo><mi>&#x1D4AB;</mi><mo>)</mo></mrow><mo>=</mo><mfrac><msup><mi>e</mi> <mrow><msub><mi>s</mi> <mrow><mi>l</mi><mi>i</mi></mrow> </msub><mrow><mo>(</mo><mi>q</mi><mo>,</mo><mi>p</mi><mo>)</mo></mrow></mrow> </msup> <mrow><msub><mo>&#x02211;</mo> <mrow><msup><mi>p</mi> <msup><mrow/> <mo>&#x27;</mo> </msup> </msup><mo>&#x02208;</mo><mi>&#x1D4AB;</mi></mrow> </msub><msup><mi>e</mi> <mrow><msub><mi>s</mi> <mrow><mi>l</mi><mi>i</mi></mrow> </msub><mrow><mo>(</mo><mi>q</mi><mo>,</mo><msup><mi>p</mi> <msup><mrow/> <mo>&#x27;</mo> </msup> </msup><mo>)</mo></mrow></mrow> </msup></mrow></mfrac><mo>.</mo></mrow></math></MathJax> inside the paragraph. */}
               <MathJax>{`\\[\\tilde{s}_{li}(q,\\mathcal {P})=\\frac{e^{s_{li}(q,p)}}{\\sum _{p^{\\prime} \\in \\mathcal {P}}e^{s_{li}(q,p^{^{\\prime }})}}.\\]`}</MathJax>
               <MathJax>{`The goal of the interaction distillation is to mimic the scoring distribution of a more expressive interaction (i.e., \\(\\tilde{s}_{de}\\)), where the loss can be measured by KL divergence as`}</MathJax>
           </p>
    </div>
  )
}

export default Test