import{j as r}from"./jsx-runtime-CDt2p4po.js";import{w as n,x as s,y as c}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const L={title:"React Aria Components/Breadcrumbs",component:n},e={render:m=>r.jsxs(n,{...m,children:[r.jsx(s,{children:r.jsx(c,{href:"/",children:"Home"})}),r.jsx(s,{children:r.jsx(c,{href:"/react-aria",children:"React Aria"})}),r.jsx(s,{children:r.jsx(c,{href:"/react-aria",children:"Breadcrumbs"})})]})};let p=[{id:"Home",url:"/"},{id:"React Aria",url:"/react-aria"},{id:"Breadcrumbs",url:"/react-aria/breadcrumbs"}];const a={render:m=>r.jsx(n,{...m,items:p,children:i=>r.jsx(s,{children:r.jsx(c,{href:i.url,children:i.id})})})};var d,t,u;e.parameters={...e.parameters,docs:{...(d=e.parameters)==null?void 0:d.docs,source:{originalSource:`{
  render: (args: any) => <Breadcrumbs {...args}>
      <Breadcrumb>
        <Link href="/">Home</Link>
      </Breadcrumb>
      <Breadcrumb>
        <Link href="/react-aria">React Aria</Link>
      </Breadcrumb>
      <Breadcrumb>
        <Link href="/react-aria">Breadcrumbs</Link>
      </Breadcrumb>
    </Breadcrumbs>
}`,...(u=(t=e.parameters)==null?void 0:t.docs)==null?void 0:u.source}}};var o,b,l;a.parameters={...a.parameters,docs:{...(o=a.parameters)==null?void 0:o.docs,source:{originalSource:`{
  render: (args: any) => <Breadcrumbs {...args} items={items}>
      {(item: ItemValue) => <Breadcrumb>
          <Link href={item.url}>{item.id}</Link>
        </Breadcrumb>}
    </Breadcrumbs>
}`,...(l=(b=a.parameters)==null?void 0:b.docs)==null?void 0:l.source}}};const g=["BreadcrumbsExample","DynamicBreadcrumbsExample"];export{e as BreadcrumbsExample,a as DynamicBreadcrumbsExample,g as __namedExportsOrder,L as default};
