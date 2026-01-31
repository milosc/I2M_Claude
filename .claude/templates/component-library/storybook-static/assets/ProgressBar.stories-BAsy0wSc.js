import{j as e}from"./jsx-runtime-CDt2p4po.js";import{ar as t,L as c}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const v={title:"React Aria Components/ProgressBar",component:t,args:{value:50},argTypes:{value:{control:"number"},minValue:{control:"number"},maxValue:{control:"number"}}},r=l=>e.jsx(t,{...l,children:({percentage:m,valueText:n})=>e.jsxs(e.Fragment,{children:[e.jsx(c,{children:"Storage space"}),e.jsx("span",{className:"value",children:n}),e.jsx("div",{className:"bar",children:e.jsx("div",{className:"fill",style:{width:m+"%"}})})]})});r.__docgenInfo={description:"",methods:[],displayName:"ProgressBarExample"};var a,s,o;r.parameters={...r.parameters,docs:{...(a=r.parameters)==null?void 0:a.docs,source:{originalSource:`args => {
  return <ProgressBar {...args}>
      {({
      percentage,
      valueText
    }) => <>
          <Label>Storage space</Label>
          <span className="value">{valueText}</span>
          <div className="bar">
            <div className="fill" style={{
          width: percentage + '%'
        }} />
          </div>
        </>}
    </ProgressBar>;
}`,...(o=(s=r.parameters)==null?void 0:s.docs)==null?void 0:o.source}}};const b=["ProgressBarExample"];export{r as ProgressBarExample,b as __namedExportsOrder,v as default};
