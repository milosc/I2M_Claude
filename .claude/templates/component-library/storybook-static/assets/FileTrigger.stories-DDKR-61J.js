import{j as e}from"./jsx-runtime-CDt2p4po.js";import{a as S}from"./index-B-lxVbXh.js";import{aO as s,B as h,y as k}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{R as w}from"./index-GiUgBvb1.js";/* empty css               */import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";const v={title:"React Aria Components/FileTrigger",component:s},r=i=>e.jsx(s,{onSelect:S("onSelect"),"data-testid":"filetrigger-example",...i,children:e.jsx(h,{children:"Upload"})}),t=i=>{let[c,j]=w.useState([]);return e.jsxs(e.Fragment,{children:[e.jsx(s,{...i,acceptDirectory:!0,onSelect:o=>{if(o){let a=[...o].map(n=>n.webkitRelativePath!==""?n.webkitRelativePath:n.name);j(a)}},children:e.jsx(h,{children:"Upload"})}),c&&e.jsx("ul",{children:c.map((o,a)=>e.jsx("li",{children:o},a))})]})},l=i=>e.jsx(s,{...i,onSelect:S("onSelect"),allowsMultiple:!0,children:e.jsx(k,{children:"Select a file"})});r.__docgenInfo={description:"",methods:[],displayName:"FileTriggerButton"};t.__docgenInfo={description:"",methods:[],displayName:"FileTriggerDirectories"};l.__docgenInfo={description:"",methods:[],displayName:"FileTriggerLinkAllowsMultiple"};var p,g,d;r.parameters={...r.parameters,docs:{...(p=r.parameters)==null?void 0:p.docs,source:{originalSource:`props => <FileTrigger onSelect={action('onSelect')} data-testid="filetrigger-example" {...props}>
    <Button>Upload</Button>
  </FileTrigger>`,...(d=(g=r.parameters)==null?void 0:g.docs)==null?void 0:d.source}}};var m,u,f;t.parameters={...t.parameters,docs:{...(m=t.parameters)==null?void 0:m.docs,source:{originalSource:`props => {
  let [files, setFiles] = React.useState<string[]>([]);
  return <>
      <FileTrigger {...props} acceptDirectory onSelect={e => {
      if (e) {
        let fileList = [...e].map(file => file.webkitRelativePath !== '' ? file.webkitRelativePath : file.name);
        setFiles(fileList);
      }
    }}>
        <Button>Upload</Button>
      </FileTrigger>
      {files && <ul>
        {files.map((file, index) => <li key={index}>{file}</li>)}
      </ul>}
    </>;
}`,...(f=(u=t.parameters)==null?void 0:u.docs)==null?void 0:f.source}}};var F,T,x;l.parameters={...l.parameters,docs:{...(F=l.parameters)==null?void 0:F.docs,source:{originalSource:`props => <FileTrigger {...props} onSelect={action('onSelect')} allowsMultiple>
    <Link>Select a file</Link>
  </FileTrigger>`,...(x=(T=l.parameters)==null?void 0:T.docs)==null?void 0:x.source}}};const A=["FileTriggerButton","FileTriggerDirectories","FileTriggerLinkAllowsMultiple"];export{r as FileTriggerButton,t as FileTriggerDirectories,l as FileTriggerLinkAllowsMultiple,A as __namedExportsOrder,v as default};
