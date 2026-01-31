import{j as e}from"./jsx-runtime-CDt2p4po.js";import{an as a,E as u,B as h,ao as x}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{R as E}from"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const C={title:"React Aria Components/Disclosure",component:a},s=o=>e.jsx(a,{...o,children:({isExpanded:i})=>e.jsxs(e.Fragment,{children:[e.jsx(u,{level:3,children:e.jsxs(h,{slot:"trigger",children:[i?"⬇️":"➡️"," This is a disclosure header"]})}),e.jsx(x,{children:e.jsx("p",{children:"This is the content of the disclosure panel."})})]})}),r=o=>{let[i,m]=E.useState(!1);return e.jsx(a,{...o,isExpanded:i,onExpandedChange:m,children:({isExpanded:g})=>e.jsxs(e.Fragment,{children:[e.jsx(u,{level:3,children:e.jsxs(h,{slot:"trigger",children:[g?"⬇️":"➡️"," This is a disclosure header"]})}),e.jsx(x,{children:e.jsx("p",{children:"This is the content of the disclosure panel."})})]})})};s.__docgenInfo={description:"",methods:[],displayName:"DisclosureExample"};r.__docgenInfo={description:"",methods:[],displayName:"DisclosureControlledExample"};var t,n,l;s.parameters={...s.parameters,docs:{...(t=s.parameters)==null?void 0:t.docs,source:{originalSource:`args => <Disclosure {...args}>
    {({
    isExpanded
  }) => <>
        <Heading level={3}>
          <Button slot="trigger">{isExpanded ? '⬇️' : '➡️'} This is a disclosure header</Button>
        </Heading>
        <DisclosurePanel>
          <p>This is the content of the disclosure panel.</p>
        </DisclosurePanel>
      </>}
  </Disclosure>`,...(l=(n=s.parameters)==null?void 0:n.docs)==null?void 0:l.source}}};var d,c,p;r.parameters={...r.parameters,docs:{...(d=r.parameters)==null?void 0:d.docs,source:{originalSource:`args => {
  let [isExpanded, setExpanded] = React.useState(false);
  return <Disclosure {...args} isExpanded={isExpanded} onExpandedChange={setExpanded}>
      {({
      isExpanded
    }) => <>
          <Heading level={3}>
            <Button slot="trigger">{isExpanded ? '⬇️' : '➡️'} This is a disclosure header</Button>
          </Heading>
          <DisclosurePanel>
            <p>This is the content of the disclosure panel.</p>
          </DisclosurePanel>
        </>}
    </Disclosure>;
}`,...(p=(c=r.parameters)==null?void 0:c.docs)==null?void 0:p.source}}};const H=["DisclosureExample","DisclosureControlledExample"];export{r as DisclosureControlledExample,s as DisclosureExample,H as __namedExportsOrder,C as default};
