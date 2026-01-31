import{j as s}from"./jsx-runtime-CDt2p4po.js";import{ap as u,B as r,an as l,E as t,ao as a}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{R as g}from"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const T={title:"React Aria Components/DisclosureGroup",component:u},i=p=>{const[o,h]=g.useState(!1),D=()=>h(e=>!e);return s.jsxs(s.Fragment,{children:[s.jsx(r,{onPress:D,children:"Toggle Disabled"}),s.jsxs(u,{...p,children:[s.jsx(l,{isDisabled:o,children:({isExpanded:e})=>s.jsxs(s.Fragment,{children:[s.jsx(t,{level:3,children:s.jsxs(r,{slot:"trigger",children:[e?"⬇️":"➡️"," This is a disclosure header"]})}),s.jsx(a,{children:s.jsx("p",{children:"This is the content of the disclosure panel."})})]})}),s.jsx(l,{isDisabled:o,children:({isExpanded:e})=>s.jsxs(s.Fragment,{children:[s.jsx(t,{level:3,children:s.jsxs(r,{slot:"trigger",children:[e?"⬇️":"➡️"," This is a disclosure header"]})}),s.jsx(a,{children:s.jsx("p",{children:"This is the content of the disclosure panel."})})]})})]})]})};i.__docgenInfo={description:"",methods:[],displayName:"DisclosureGroupExample"};var n,d,c;i.parameters={...i.parameters,docs:{...(n=i.parameters)==null?void 0:n.docs,source:{originalSource:`args => {
  const [isDisabled, setIsDisabled] = React.useState(false);
  const toggleDisabled = () => setIsDisabled(d => !d);
  return <>
      <Button onPress={toggleDisabled}>Toggle Disabled</Button>
      <DisclosureGroup {...args}>
        <Disclosure isDisabled={isDisabled}>
          {({
          isExpanded
        }) => <>
              <Heading level={3}>
                <Button slot="trigger">
                  {isExpanded ? '⬇️' : '➡️'} This is a disclosure header
                </Button>
              </Heading>
              <DisclosurePanel>
                <p>This is the content of the disclosure panel.</p>
              </DisclosurePanel>
            </>}
        </Disclosure>
        <Disclosure isDisabled={isDisabled}>
          {({
          isExpanded
        }) => <>
              <Heading level={3}>
                <Button slot="trigger">
                  {isExpanded ? '⬇️' : '➡️'} This is a disclosure header
                </Button>
              </Heading>
              <DisclosurePanel>
                <p>This is the content of the disclosure panel.</p>
              </DisclosurePanel>
            </>}
        </Disclosure>
      </DisclosureGroup>
    </>;
}`,...(c=(d=i.parameters)==null?void 0:d.docs)==null?void 0:c.source}}};const B=["DisclosureGroupExample"];export{i as DisclosureGroupExample,B as __namedExportsOrder,T as default};
