import{j as e}from"./jsx-runtime-CDt2p4po.js";import{f as m,L as n,B as r,g as d,P as c,O as v,b as u,o as re,au as oe,V as Q,_ as le,T as ne,I as me,Z as S,h as de,ad as ce}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";import{a as ee,$ as ue}from"./ListLayout-8Q9Kcx4Y.js";import{a,L as ie}from"./utils-N1pTmi3h.js";import{s as o}from"./index.module-B9nxguEg.js";/* empty css               */import"./index-C8NrMXaH.js";const Me={title:"React Aria Components/Select",component:m,argTypes:{validationBehavior:{control:"select",options:["native","aria"]},selectionMode:{control:"radio",options:["single","multiple"]}}},p=i=>e.jsxs(m,{...i,"data-testid":"select-example",id:"select-example-id",children:[e.jsx(n,{style:{display:"block"},children:"Test"}),e.jsxs(r,{children:[e.jsx(d,{}),e.jsx("span",{"aria-hidden":"true",style:{paddingLeft:5},children:"▼"})]}),e.jsxs(c,{children:[e.jsx(v,{children:e.jsx("svg",{width:12,height:12,children:e.jsx("path",{d:"M0 0,L6 6,L12 0"})})}),e.jsxs(u,{className:o.menu,children:[e.jsx(a,{children:"Foo"}),e.jsx(a,{children:"Bar"}),e.jsx(a,{children:"Baz"}),e.jsx(a,{href:"http://google.com",children:"Google"})]})]})]}),h=i=>e.jsx(m,{...i,"data-testid":"select-render-props",children:({isOpen:t})=>e.jsxs(e.Fragment,{children:[e.jsx(n,{style:{display:"block"},children:"Test"}),e.jsxs(r,{children:[e.jsx(d,{children:({selectedItems:s,defaultChildren:l})=>s.length<=1?l:`${s.length} selected items`}),e.jsx("span",{"aria-hidden":"true",style:{paddingLeft:5},children:t?"▲":"▼"})]}),e.jsx(c,{children:e.jsxs(u,{className:o.menu,children:[e.jsx(a,{children:"Foo"}),e.jsx(a,{children:"Bar"}),e.jsx(a,{children:"Baz"}),e.jsx(a,{href:"http://google.com",children:"Google"})]})})]})}),x=i=>e.jsxs(m,{...i,"data-testid":"select-example",id:"select-example-id",children:[e.jsx(n,{style:{display:"block"},children:"States"}),e.jsxs("div",{style:{display:"flex",gap:8,alignItems:"start",maxWidth:250},children:[e.jsx(d,{children:({selectedItems:t,state:s})=>e.jsx(re,{"aria-label":"Selected states",items:t,renderEmptyState:()=>"No selected items",onRemove:l=>{for(let B of l)s.selectionManager.toggleSelection(B)},children:l=>e.jsx(oe,{children:l.name})})}),e.jsx(r,{children:"+"})]}),e.jsx(c,{placement:"bottom end",children:e.jsx(u,{className:o.menu,items:te,children:t=>e.jsx(a,{children:t.name})})})]});let ae=i=>Array.from({length:i},(t,s)=>({id:s,name:`Item ${s}`})),pe=ae(100);const te=[{id:"AL",name:"Alabama"},{id:"AK",name:"Alaska"},{id:"AS",name:"American Samoa"},{id:"AZ",name:"Arizona"},{id:"AR",name:"Arkansas"},{id:"CA",name:"California"},{id:"CO",name:"Colorado"},{id:"CT",name:"Connecticut"},{id:"DE",name:"Delaware"},{id:"DC",name:"District Of Columbia"},{id:"FM",name:"Federated States Of Micronesia"},{id:"FL",name:"Florida"},{id:"GA",name:"Georgia"},{id:"GU",name:"Guam"},{id:"HI",name:"Hawaii"},{id:"ID",name:"Idaho"},{id:"IL",name:"Illinois"},{id:"IN",name:"Indiana"},{id:"IA",name:"Iowa"},{id:"KS",name:"Kansas"},{id:"KY",name:"Kentucky"},{id:"LA",name:"Louisiana"},{id:"ME",name:"Maine"},{id:"MH",name:"Marshall Islands"},{id:"MD",name:"Maryland"},{id:"MA",name:"Massachusetts"},{id:"MI",name:"Michigan"},{id:"MN",name:"Minnesota"},{id:"MS",name:"Mississippi"},{id:"MO",name:"Missouri"},{id:"MT",name:"Montana"},{id:"NE",name:"Nebraska"},{id:"NV",name:"Nevada"},{id:"NH",name:"New Hampshire"},{id:"NJ",name:"New Jersey"},{id:"NM",name:"New Mexico"},{id:"NY",name:"New York"},{id:"NC",name:"North Carolina"},{id:"ND",name:"North Dakota"},{id:"MP",name:"Northern Mariana Islands"},{id:"OH",name:"Ohio"},{id:"OK",name:"Oklahoma"},{id:"OR",name:"Oregon"},{id:"PW",name:"Palau"},{id:"PA",name:"Pennsylvania"},{id:"PR",name:"Puerto Rico"},{id:"RI",name:"Rhode Island"},{id:"SC",name:"South Carolina"},{id:"SD",name:"South Dakota"},{id:"TN",name:"Tennessee"},{id:"TX",name:"Texas"},{id:"UT",name:"Utah"},{id:"VT",name:"Vermont"},{id:"VI",name:"Virgin Islands"},{id:"VA",name:"Virginia"},{id:"WA",name:"Washington"},{id:"WV",name:"West Virginia"},{id:"WI",name:"Wisconsin"},{id:"WY",name:"Wyoming"}],g=i=>e.jsxs(m,{...i,children:[e.jsx(n,{style:{display:"block"},children:"Test"}),e.jsxs(r,{children:[e.jsx(d,{}),e.jsx("span",{"aria-hidden":"true",style:{paddingLeft:5},children:"▼"})]}),e.jsxs(c,{children:[e.jsx(v,{children:e.jsx("svg",{width:12,height:12,children:e.jsx("path",{d:"M0 0,L6 6,L12 0"})})}),e.jsx(u,{items:te,className:o.menu,children:t=>e.jsx(a,{children:t.name})})]})]}),y=i=>e.jsxs(m,{...i,children:[e.jsx(n,{style:{display:"block"},children:"Test"}),e.jsxs(r,{children:[e.jsx(d,{}),e.jsx("span",{"aria-hidden":"true",style:{paddingLeft:5},children:"▼"})]}),e.jsxs(c,{children:[e.jsx(v,{children:e.jsx("svg",{width:12,height:12,children:e.jsx("path",{d:"M0 0,L6 6,L12 0"})})}),e.jsx(Q,{layout:new ee({rowHeight:25}),children:e.jsx(u,{items:pe,className:o.menu,children:t=>e.jsx(a,{children:t.name})})})]})]}),he=i=>e.jsx(ce,{style:{height:30,width:"100%"},...i,children:e.jsx(ie,{style:{height:20,width:20,transform:"translate(-50%, -50%)"}})});function xe(i){let t=ue({async load({signal:s,cursor:l}){l&&(l=l.replace(/^http:\/\//i,"https://")),await new Promise(se=>setTimeout(se,i.delay));let M=await(await fetch(l||"https://swapi.py4e.com/api/people/?search=",{signal:s})).json();return{items:M.results,cursor:M.next}}});return e.jsxs(m,{children:[e.jsx(n,{style:{display:"block"},children:"Async Virtualized Collection render Select"}),e.jsxs(r,{children:[e.jsx(d,{}),t.isLoading&&e.jsx(ie,{style:{right:"20px",left:"unset",top:"0px",height:"100%",width:20}}),e.jsx("span",{"aria-hidden":"true",style:{paddingLeft:25},children:"▼"})]}),e.jsx(Q,{layout:ee,layoutOptions:{rowHeight:25,loaderHeight:30},children:e.jsxs(c,{children:[e.jsx(v,{children:e.jsx("svg",{width:12,height:12,children:e.jsx("path",{d:"M0 0,L6 6,L12 0"})})}),e.jsxs(u,{className:o.menu,children:[e.jsx(de,{items:t.items,children:s=>e.jsx(a,{id:s.name,children:s.name})}),e.jsx(he,{isLoading:t.loadingState==="loadingMore",onLoadMore:t.loadMore})]})]})})]})}const b={render:i=>e.jsx(xe,{...i}),args:{delay:50}},j=i=>e.jsxs(le,{children:[e.jsxs(ne,{isRequired:!0,autoComplete:"username",className:o.textfieldExample,name:"username",children:[e.jsx(n,{children:"Username"}),e.jsx(me,{}),e.jsx(S,{className:o.errorMessage})]}),e.jsxs(m,{...i,isRequired:!0,autoComplete:"organization",name:"company",children:[e.jsx(n,{style:{display:"block"},children:"Company"}),e.jsxs(r,{children:[e.jsx(d,{}),e.jsx("span",{"aria-hidden":"true",style:{paddingLeft:5},children:"▼"})]}),e.jsxs(c,{children:[e.jsx(v,{children:e.jsx("svg",{height:12,width:12,children:e.jsx("path",{d:"M0 0,L6 6,L12 0"})})}),e.jsxs(u,{className:o.menu,children:[e.jsx(a,{children:"Adobe"}),e.jsx(a,{children:"Google"}),e.jsx(a,{children:"Microsoft"})]})]}),e.jsx(S,{className:o.errorMessage})]}),e.jsx(r,{type:"submit",children:"Submit"}),e.jsx(r,{type:"reset",children:"Reset"})]}),L=i=>e.jsxs("form",{children:[e.jsxs(m,{...i,name:"select",isRequired:!0,children:[e.jsx(n,{style:{display:"block"},children:"Required Select with many items"}),e.jsxs(r,{children:[e.jsx(d,{}),e.jsx("span",{"aria-hidden":"true",style:{paddingLeft:5},children:"▼"})]}),e.jsx(S,{}),e.jsx(c,{children:e.jsx(u,{items:ae(301),className:o.menu,children:t=>e.jsx(a,{children:t.name})})})]}),e.jsx(r,{type:"submit",children:"Submit"})]}),f=()=>e.jsxs("div",{style:{display:"flex",flexDirection:"row",height:"100vh"},children:[e.jsx("div",{style:{flex:3},children:"Scrolling here should do nothing."}),e.jsxs("div",{style:{flex:1,overflowY:"auto"},children:["Scrolling here should scroll the right side.",e.jsx("br",{}),e.jsx("br",{}),e.jsx("br",{}),e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),e.jsx("br",{}),e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),e.jsx("br",{}),e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),e.jsx("br",{}),e.jsx("br",{}),"Lorem ipsum dolor sit amet consectetur adipisicing elit. Error voluptatibus esse qui enim neque aliquam facere velit ipsa non, voluptates aperiam odit minima dolorum harum! Facere eligendi officia ipsam mollitia!",e.jsx("br",{}),e.jsx("br",{}),e.jsx("br",{}),e.jsxs(m,{children:[e.jsx(n,{children:"Favorite Animal"}),e.jsxs(r,{children:[e.jsx(d,{}),e.jsx("span",{"aria-hidden":"true",children:"▼"})]}),e.jsx(c,{children:e.jsxs(u,{children:[e.jsx(a,{children:"Cat"}),e.jsx(a,{children:"Dog"}),e.jsx(a,{children:"Kangaroo"})]})})]})]})]});p.__docgenInfo={description:"",methods:[],displayName:"SelectExample"};h.__docgenInfo={description:"",methods:[],displayName:"SelectRenderProps"};x.__docgenInfo={description:"",methods:[],displayName:"SelectWithTagGroup"};g.__docgenInfo={description:"",methods:[],displayName:"SelectManyItems"};y.__docgenInfo={description:"",methods:[],displayName:"VirtualizedSelect"};j.__docgenInfo={description:"",methods:[],displayName:"SelectSubmitExample"};L.__docgenInfo={description:"",methods:[],displayName:"RequiredSelectWithManyItems"};f.__docgenInfo={description:"",methods:[],displayName:"SelectScrollBug"};var I,q,N;p.parameters={...p.parameters,docs:{...(I=p.parameters)==null?void 0:I.docs,source:{originalSource:`args => <Select {...args} data-testid="select-example" id="select-example-id">
    <Label style={{
    display: 'block'
  }}>Test</Label>
    <Button>
      <SelectValue />
      <span aria-hidden="true" style={{
      paddingLeft: 5
    }}>▼</span>
    </Button>
    <Popover>
      <OverlayArrow>
        <svg width={12} height={12}><path d="M0 0,L6 6,L12 0" /></svg>
      </OverlayArrow>
      <ListBox className={styles.menu}>
        <MyListBoxItem>Foo</MyListBoxItem>
        <MyListBoxItem>Bar</MyListBoxItem>
        <MyListBoxItem>Baz</MyListBoxItem>
        <MyListBoxItem href="http://google.com">Google</MyListBoxItem>
      </ListBox>
    </Popover>
  </Select>`,...(N=(q=p.parameters)==null?void 0:q.docs)==null?void 0:N.source}}};var F,w,E;h.parameters={...h.parameters,docs:{...(F=h.parameters)==null?void 0:F.docs,source:{originalSource:`args => <Select {...args} data-testid="select-render-props">
    {({
    isOpen
  }) => <>
        <Label style={{
      display: 'block'
    }}>Test</Label>
        <Button>
          <SelectValue>
            {({
          selectedItems,
          defaultChildren
        }) => selectedItems.length <= 1 ? defaultChildren : \`\${selectedItems.length} selected items\`}
          </SelectValue>
          <span aria-hidden="true" style={{
        paddingLeft: 5
      }}>{isOpen ? '▲' : '▼'}</span>
        </Button>
        <Popover>
          <ListBox className={styles.menu}>
            <MyListBoxItem>Foo</MyListBoxItem>
            <MyListBoxItem>Bar</MyListBoxItem>
            <MyListBoxItem>Baz</MyListBoxItem>
            <MyListBoxItem href="http://google.com">Google</MyListBoxItem>
          </ListBox>
        </Popover>
      </>}
  </Select>`,...(E=(w=h.parameters)==null?void 0:w.docs)==null?void 0:E.source}}};var A,R,V;x.parameters={...x.parameters,docs:{...(A=x.parameters)==null?void 0:A.docs,source:{originalSource:`args => <Select {...args} data-testid="select-example" id="select-example-id">
    <Label style={{
    display: 'block'
  }}>States</Label>
    <div style={{
    display: 'flex',
    gap: 8,
    alignItems: 'start',
    maxWidth: 250
  }}>
      <SelectValue>
        {({
        selectedItems,
        state
      }) => <TagGroup aria-label="Selected states" items={selectedItems as {
        name: string;
      }[]} renderEmptyState={() => 'No selected items'} onRemove={keys => {
        for (let key of keys) {
          state.selectionManager.toggleSelection(key);
        }
      }}>
            {item => <Tag>{item.name}</Tag>}
          </TagGroup>}
      </SelectValue>
      <Button>+</Button>
    </div>
    <Popover placement="bottom end">
      <ListBox className={styles.menu} items={usStateOptions}>
        {state => <MyListBoxItem>{state.name}</MyListBoxItem>}
      </ListBox>
    </Popover>
  </Select>`,...(V=(R=x.parameters)==null?void 0:R.docs)==null?void 0:V.source}}};var T,k,P;g.parameters={...g.parameters,docs:{...(T=g.parameters)==null?void 0:T.docs,source:{originalSource:`args => <Select {...args}>
    <Label style={{
    display: 'block'
  }}>Test</Label>
    <Button>
      <SelectValue />
      <span aria-hidden="true" style={{
      paddingLeft: 5
    }}>▼</span>
    </Button>
    <Popover>
      <OverlayArrow>
        <svg width={12} height={12}><path d="M0 0,L6 6,L12 0" /></svg>
      </OverlayArrow>
      <ListBox items={usStateOptions} className={styles.menu}>
        {item => <MyListBoxItem>{item.name}</MyListBoxItem>}
      </ListBox>
    </Popover>
  </Select>`,...(P=(k=g.parameters)==null?void 0:k.docs)==null?void 0:P.source}}};var C,O,_;y.parameters={...y.parameters,docs:{...(C=y.parameters)==null?void 0:C.docs,source:{originalSource:`args => <Select {...args}>
    <Label style={{
    display: 'block'
  }}>Test</Label>
    <Button>
      <SelectValue />
      <span aria-hidden="true" style={{
      paddingLeft: 5
    }}>▼</span>
    </Button>
    <Popover>
      <OverlayArrow>
        <svg width={12} height={12}><path d="M0 0,L6 6,L12 0" /></svg>
      </OverlayArrow>
      <Virtualizer layout={new ListLayout({
      rowHeight: 25
    })}>
        <ListBox items={manyItems} className={styles.menu}>
          {item => <MyListBoxItem>{item.name}</MyListBoxItem>}
        </ListBox>
      </Virtualizer>
    </Popover>
  </Select>`,...(_=(O=y.parameters)==null?void 0:O.docs)==null?void 0:_.source}}};var z,W,G;b.parameters={...b.parameters,docs:{...(z=b.parameters)==null?void 0:z.docs,source:{originalSource:`{
  render: args => <AsyncVirtualizedCollectionRenderSelectRender {...args} />,
  args: {
    delay: 50
  }
}`,...(G=(W=b.parameters)==null?void 0:W.docs)==null?void 0:G.source}}};var D,$,H;j.parameters={...j.parameters,docs:{...(D=j.parameters)==null?void 0:D.docs,source:{originalSource:`args => <Form>
    <TextField isRequired autoComplete="username" className={styles.textfieldExample} name="username">
      <Label>Username</Label>
      <Input />
      <FieldError className={styles.errorMessage} />
    </TextField>
    <Select {...args} isRequired autoComplete="organization" name="company">
      <Label style={{
      display: 'block'
    }}>Company</Label>
      <Button>
        <SelectValue />
        <span aria-hidden="true" style={{
        paddingLeft: 5
      }}>
          ▼
        </span>
      </Button>
      <Popover>
        <OverlayArrow>
          <svg height={12} width={12}>
            <path d="M0 0,L6 6,L12 0" />
          </svg>
        </OverlayArrow>
        <ListBox className={styles.menu}>
          <MyListBoxItem>Adobe</MyListBoxItem>
          <MyListBoxItem>Google</MyListBoxItem>
          <MyListBoxItem>Microsoft</MyListBoxItem>
        </ListBox>
      </Popover>
      <FieldError className={styles.errorMessage} />
    </Select>
    <Button type="submit">Submit</Button>
    <Button type="reset">Reset</Button>
  </Form>`,...(H=($=j.parameters)==null?void 0:$.docs)==null?void 0:H.source}}};var K,Y,U;L.parameters={...L.parameters,docs:{...(K=L.parameters)==null?void 0:K.docs,source:{originalSource:`props => <form>
    <Select {...props} name="select" isRequired>
      <Label style={{
      display: 'block'
    }}>Required Select with many items</Label>
      <Button>
        <SelectValue />
        <span aria-hidden="true" style={{
        paddingLeft: 5
      }}>▼</span>
      </Button>
      <FieldError />
      <Popover>
        <ListBox items={makeItems(301)} className={styles.menu}>
          {item => <MyListBoxItem>{item.name}</MyListBoxItem>}
        </ListBox>
      </Popover>
    </Select>
    <Button type="submit">Submit</Button>
  </form>`,...(U=(Y=L.parameters)==null?void 0:Y.docs)==null?void 0:U.source}}};var J,Z,X;f.parameters={...f.parameters,docs:{...(J=f.parameters)==null?void 0:J.docs,source:{originalSource:`() => {
  return <div style={{
    display: 'flex',
    flexDirection: 'row',
    height: '100vh'
  }}>
      <div style={{
      flex: 3
    }}>
        Scrolling here should do nothing.
      </div>

      <div style={{
      flex: 1,
      overflowY: 'auto'
    }}>
        Scrolling here should scroll the right side.
        <br />
        <br />
        <br />
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        <br />
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        <br />
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        <br />
        <br />
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Error
        voluptatibus esse qui enim neque aliquam facere velit ipsa non,
        voluptates aperiam odit minima dolorum harum! Facere eligendi officia
        ipsam mollitia!
        <br />
        <br />
        <br />
        <Select>
          <Label>Favorite Animal</Label>
          <Button>
            <SelectValue />
            <span aria-hidden="true">▼</span>
          </Button>
          <Popover>
            <ListBox>
              <MyListBoxItem>Cat</MyListBoxItem>
              <MyListBoxItem>Dog</MyListBoxItem>
              <MyListBoxItem>Kangaroo</MyListBoxItem>
            </ListBox>
          </Popover>
        </Select>
      </div>
    </div>;
}`,...(X=(Z=f.parameters)==null?void 0:Z.docs)==null?void 0:X.source}}};const Ie=["SelectExample","SelectRenderProps","SelectWithTagGroup","SelectManyItems","VirtualizedSelect","AsyncVirtualizedCollectionRenderSelect","SelectSubmitExample","RequiredSelectWithManyItems","SelectScrollBug"];export{b as AsyncVirtualizedCollectionRenderSelect,L as RequiredSelectWithManyItems,p as SelectExample,g as SelectManyItems,h as SelectRenderProps,f as SelectScrollBug,j as SelectSubmitExample,x as SelectWithTagGroup,y as VirtualizedSelect,Ie as __namedExportsOrder,Me as default};
