import{j as m}from"./jsx-runtime-CDt2p4po.js";import{a as e}from"./index-B-lxVbXh.js";import{c as p}from"./utils-N1pTmi3h.js";import{r as c}from"./index-GiUgBvb1.js";import{s as g}from"./index.module-B9nxguEg.js";import{b0 as l}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";/* empty css               */import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";const b={title:"React Aria Components/ToggleButton",component:l},o=()=>{const[n,t]=c.useState("black");return m.jsx(l,{className:p(g,"toggleButtonExample"),"data-testid":"toggle-button-example",onKeyUp:e("keyup"),onPress:e("press"),onHoverStart:()=>t("red"),onHoverEnd:()=>t("black"),style:{color:n},children:"Toggle"})};o.__docgenInfo={description:"",methods:[],displayName:"ToggleButtonExample"};var r,s,a;o.parameters={...o.parameters,docs:{...(r=o.parameters)==null?void 0:r.docs,source:{originalSource:`() => {
  const [textColor, setTextColor] = useState('black');
  return <ToggleButton className={classNames(styles, 'toggleButtonExample')} data-testid="toggle-button-example" onKeyUp={action('keyup')} onPress={action('press')} onHoverStart={() => setTextColor('red')} onHoverEnd={() => setTextColor('black')} style={{
    color: textColor
  }}>
      Toggle
    </ToggleButton>;
}`,...(a=(s=o.parameters)==null?void 0:s.docs)==null?void 0:a.source}}};const k=["ToggleButtonExample"];export{o as ToggleButtonExample,k as __namedExportsOrder,b as default};
