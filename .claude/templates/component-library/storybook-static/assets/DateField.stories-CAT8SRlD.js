import{j as e}from"./jsx-runtime-CDt2p4po.js";import{a as f}from"./index-B-lxVbXh.js";import{ae as d,af as y,ag as n,L as i,ah as D,ai as g,Z as F,aj as r,_ as j,T as V,I as T,B as L}from"./Virtualizer-43kePMo2.js";import{c as h}from"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";import{s as l}from"./index.module-B9nxguEg.js";/* empty css               */import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";const _={title:"React Aria Components/DateField",argTypes:{onChange:{table:{disable:!0}},granularity:{control:"select",options:["day","hour","minute","second"]},minValue:{control:"date"},maxValue:{control:"date"},isRequired:{control:"boolean"},isInvalid:{control:"boolean"},isDisabled:{control:"boolean"},isReadOnly:{control:"boolean"},validationBehavior:{control:"select",options:["native","aria"]}},args:{onChange:f("OnChange")},component:d},s=t=>e.jsxs(d,{...t,minValue:t.minValue?n(t.minValue,r()):void 0,maxValue:t.maxValue?n(t.maxValue,r()):void 0,"data-testid":"date-field-example",defaultValue:y("2024-01-01T01:01:00Z"),children:[e.jsx(i,{style:{display:"block"},children:"Date"}),e.jsx(D,{className:l.field,"data-testid2":"date-input",children:a=>e.jsx(g,{segment:a,className:h(l.segment,{[l.placeholder]:a.isPlaceholder})})}),e.jsx(F,{style:{display:"block"}})]}),o=t=>e.jsxs(j,{onSubmit:a=>{f("onSubmit")(Object.fromEntries(new FormData(a.target).entries())),a.preventDefault()},children:[e.jsxs(V,{children:[e.jsx(i,{children:"Name"}),e.jsx(T,{name:"name",type:"text",id:"name",autoComplete:"name"})]}),e.jsxs(d,{...t,name:"bday",autoComplete:"bday",defaultValue:y("2021-04-07T18:45:22Z"),"data-testid":"date-field-example",children:[e.jsx(i,{style:{display:"block"},children:"Date"}),e.jsx(D,{className:l.field,"data-testid2":"date-input",children:a=>e.jsx(g,{segment:a,className:h(l.segment,{[l.placeholder]:a.isPlaceholder})})}),e.jsx(F,{style:{display:"block"}})]}),e.jsx(L,{type:"submit",children:"Submit"})]});s.__docgenInfo={description:"",methods:[],displayName:"DateFieldExample"};o.__docgenInfo={description:"",methods:[],displayName:"DateFieldAutoFill"};var m,c,p;s.parameters={...s.parameters,docs:{...(m=s.parameters)==null?void 0:m.docs,source:{originalSource:`props => <DateField {...props} minValue={props.minValue ? fromAbsolute(props.minValue, getLocalTimeZone()) : undefined} maxValue={props.maxValue ? fromAbsolute(props.maxValue, getLocalTimeZone()) : undefined} data-testid="date-field-example" defaultValue={parseAbsoluteToLocal('2024-01-01T01:01:00Z')}>
    <Label style={{
    display: 'block'
  }}>Date</Label>
    <DateInput className={styles.field} data-testid2="date-input">
      {segment => <DateSegment segment={segment} className={clsx(styles.segment, {
      [styles.placeholder]: segment.isPlaceholder
    })} />}
    </DateInput>
    <FieldError style={{
    display: 'block'
  }} />
  </DateField>`,...(p=(c=s.parameters)==null?void 0:c.docs)==null?void 0:p.source}}};var u,b,x;o.parameters={...o.parameters,docs:{...(u=o.parameters)==null?void 0:u.docs,source:{originalSource:`props => <Form onSubmit={e => {
  action('onSubmit')(Object.fromEntries(new FormData(e.target as HTMLFormElement).entries()));
  e.preventDefault();
}}>
    <TextField>
      <Label>Name</Label>
      <Input name="name" type="text" id="name" autoComplete="name" />
    </TextField>
    <DateField {...props} name="bday" autoComplete="bday" defaultValue={parseAbsoluteToLocal('2021-04-07T18:45:22Z')} data-testid="date-field-example">
      <Label style={{
      display: 'block'
    }}>Date</Label>
      <DateInput className={styles.field} data-testid2="date-input">
        {segment => <DateSegment segment={segment} className={clsx(styles.segment, {
        [styles.placeholder]: segment.isPlaceholder
      })} />}
      </DateInput>
      <FieldError style={{
      display: 'block'
    }} />
    </DateField>
    <Button type="submit">Submit</Button>
  </Form>`,...(x=(b=o.parameters)==null?void 0:b.docs)==null?void 0:x.source}}};const Z=["DateFieldExample","DateFieldAutoFill"];export{o as DateFieldAutoFill,s as DateFieldExample,Z as __namedExportsOrder,_ as default};
