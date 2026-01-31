import{j as e}from"./jsx-runtime-CDt2p4po.js";import{aP as l,L as c}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const v={title:"React Aria Components/Meter",component:l,args:{value:50},argTypes:{value:{control:"number"},minValue:{control:"number"},maxValue:{control:"number"}}},a=o=>e.jsx(l,{...o,children:({percentage:m,valueText:n})=>e.jsxs(e.Fragment,{children:[e.jsx(c,{children:"Storage space"}),e.jsx("span",{className:"value",children:n}),e.jsx("div",{className:"bar",children:e.jsx("div",{className:"fill",style:{width:m+"%"}})})]})});a.__docgenInfo={description:"",methods:[],displayName:"MeterExample"};var r,s,t;a.parameters={...a.parameters,docs:{...(r=a.parameters)==null?void 0:r.docs,source:{originalSource:`args => {
  return <Meter {...args}>
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
    </Meter>;
}`,...(t=(s=a.parameters)==null?void 0:s.docs)==null?void 0:t.source}}};const b=["MeterExample"];export{a as MeterExample,b as __namedExportsOrder,v as default};
