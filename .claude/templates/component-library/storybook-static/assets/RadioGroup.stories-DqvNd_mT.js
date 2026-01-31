import{j as a}from"./jsx-runtime-CDt2p4po.js";import{a as r}from"./index-B-lxVbXh.js";import{aR as t,L as i,aS as e,D as G,B as s,aw as E,ax as S,a4 as L,_ as g,Z as m}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{r as A}from"./index-GiUgBvb1.js";import{s as o}from"./index.module-B9nxguEg.js";/* empty css               */import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";const P={title:"React Aria Components/RadioGroup",component:t},u={render:d=>a.jsxs(t,{...d,"data-testid":"radio-group-example",className:o.radiogroup,children:[a.jsx(i,{children:"Favorite pet"}),a.jsx(e,{onFocus:r("radio focus"),onBlur:r("radio blur"),className:o.radio,value:"dogs","data-testid":"radio-dog",children:"Dog"}),a.jsx(e,{onFocus:r("radio focus"),onBlur:r("radio blur"),className:o.radio,value:"cats",children:"Cat"}),a.jsx(e,{onFocus:r("radio focus"),onBlur:r("radio blur"),className:o.radio,value:"dragon",children:"Dragon"})]}),args:{onFocus:r("onFocus"),onBlur:r("onBlur")}},l=d=>{let[p,C]=A.useState(null);return a.jsxs(t,{...d,"data-testid":"radio-group-example",className:o.radiogroup,value:p,onChange:C,children:[a.jsx(i,{children:"Favorite pet (controlled)"}),a.jsx(e,{className:o.radio,value:"dogs","data-testid":"radio-dog",children:"Dog"}),a.jsx(e,{className:o.radio,value:"cats",children:"Cat"}),a.jsx(e,{className:o.radio,value:"dragon",children:"Dragon"})]})},n=d=>a.jsxs(G,{children:[a.jsx(s,{children:"Open dialog"}),a.jsx(E,{style:{position:"fixed",zIndex:100,top:0,left:0,bottom:0,right:0,background:"rgba(0, 0, 0, 0.5)",display:"flex",alignItems:"center",justifyContent:"center"},children:a.jsx(S,{style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:30},children:a.jsx(L,{style:{outline:"2px solid transparent",outlineOffset:"2px",position:"relative"},children:({close:p})=>a.jsxs("div",{style:{display:"flex",flexDirection:"column",gap:10},children:[a.jsxs("div",{style:{display:"flex",flexDirection:"row",gap:20},children:[a.jsx("div",{children:a.jsxs(t,{...d,"data-testid":"radio-group-example",className:o.radiogroup,children:[a.jsx(i,{children:"Favorite pet"}),a.jsx(e,{className:o.radio,value:"dogs","data-testid":"radio-dog",children:"Dog"}),a.jsx(e,{className:o.radio,value:"cats",children:"Cat"}),a.jsx(e,{className:o.radio,value:"dragon",children:"Dragon"})]})}),a.jsx(g,{children:a.jsxs(t,{className:o.radiogroup,"data-testid":"radio-group-example-2",isRequired:!0,children:[a.jsx(i,{children:"Second Favorite pet"}),a.jsx(e,{className:o.radio,value:"dogs","data-testid":"radio-dog",children:"Dog"}),a.jsx(s,{children:"About dogs"}),a.jsx(e,{className:o.radio,value:"cats",children:"Cat"}),a.jsx(s,{children:"About cats"}),a.jsx(e,{className:o.radio,value:"dragon",children:"Dragon"}),a.jsx(s,{children:"About dragons"}),a.jsx(m,{className:o.errorMessage})]})}),a.jsx(g,{children:a.jsxs(t,{className:o.radiogroup,"data-testid":"radio-group-example-3",defaultValue:"dragon",isRequired:!0,children:[a.jsx(i,{children:"Third Favorite pet"}),a.jsx(e,{className:o.radio,value:"dogs","data-testid":"radio-dog",children:"Dog"}),a.jsx(s,{children:"About dogs"}),a.jsx(e,{className:o.radio,value:"cats",children:"Cat"}),a.jsx(s,{children:"About cats"}),a.jsx(e,{className:o.radio,value:"dragon",children:"Dragon"}),a.jsx(s,{children:"About dragons"}),a.jsx(m,{className:o.errorMessage})]})})]}),a.jsx("div",{children:a.jsx(s,{onPress:p,style:{marginTop:10},children:"Close"})})]})})})})]}),c=d=>a.jsxs(g,{children:[a.jsxs(t,{...d,className:o.radiogroup,"data-testid":"radio-group-example",isRequired:!0,children:[a.jsx(i,{children:"Favorite pet"}),a.jsx(e,{className:o.radio,value:"dogs","data-testid":"radio-dog",children:"Dog"}),a.jsx(e,{className:o.radio,value:"cats",children:"Cat"}),a.jsx(e,{className:o.radio,value:"dragon",children:"Dragon"}),a.jsx(m,{className:o.errorMessage})]}),a.jsx(s,{type:"submit",children:"Submit"}),a.jsx(s,{type:"reset",children:"Reset"})]});l.__docgenInfo={description:"",methods:[],displayName:"RadioGroupControlledExample"};n.__docgenInfo={description:"",methods:[],displayName:"RadioGroupInDialogExample"};c.__docgenInfo={description:"",methods:[],displayName:"RadioGroupSubmitExample"};var x,R,v;u.parameters={...u.parameters,docs:{...(x=u.parameters)==null?void 0:x.docs,source:{originalSource:`{
  render: props => {
    return <RadioGroup {...props} data-testid="radio-group-example" className={styles.radiogroup}>
        <Label>Favorite pet</Label>
        <Radio onFocus={action('radio focus')} onBlur={action('radio blur')} className={styles.radio} value="dogs" data-testid="radio-dog">Dog</Radio>
        <Radio onFocus={action('radio focus')} onBlur={action('radio blur')} className={styles.radio} value="cats">Cat</Radio>
        <Radio onFocus={action('radio focus')} onBlur={action('radio blur')} className={styles.radio} value="dragon">Dragon</Radio>
      </RadioGroup>;
  },
  args: {
    onFocus: action('onFocus'),
    onBlur: action('onBlur')
  }
}`,...(v=(R=u.parameters)==null?void 0:R.docs)==null?void 0:v.source}}};var h,y,j;l.parameters={...l.parameters,docs:{...(h=l.parameters)==null?void 0:h.docs,source:{originalSource:`props => {
  let [selected, setSelected] = useState<string | null>(null);
  return <RadioGroup {...props} data-testid="radio-group-example" className={styles.radiogroup} value={selected} onChange={setSelected}>
      <Label>Favorite pet (controlled)</Label>
      <Radio className={styles.radio} value="dogs" data-testid="radio-dog">Dog</Radio>
      <Radio className={styles.radio} value="cats">Cat</Radio>
      <Radio className={styles.radio} value="dragon">Dragon</Radio>
    </RadioGroup>;
}`,...(j=(y=l.parameters)==null?void 0:y.docs)==null?void 0:j.source}}};var N,b,D;n.parameters={...n.parameters,docs:{...(N=n.parameters)==null?void 0:N.docs,source:{originalSource:`props => {
  return <DialogTrigger>
      <Button>Open dialog</Button>
      <ModalOverlay style={{
      position: 'fixed',
      zIndex: 100,
      top: 0,
      left: 0,
      bottom: 0,
      right: 0,
      background: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
        <Modal style={{
        background: 'Canvas',
        color: 'CanvasText',
        border: '1px solid gray',
        padding: 30
      }}>
          <Dialog style={{
          outline: '2px solid transparent',
          outlineOffset: '2px',
          position: 'relative'
        }}>
            {({
            close
          }) => <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 10
          }}>
                <div style={{
              display: 'flex',
              flexDirection: 'row',
              gap: 20
            }}>
                  <div>
                    <RadioGroup {...props} data-testid="radio-group-example" className={styles.radiogroup}>
                      <Label>Favorite pet</Label>
                      <Radio className={styles.radio} value="dogs" data-testid="radio-dog">Dog</Radio>
                      <Radio className={styles.radio} value="cats">Cat</Radio>
                      <Radio className={styles.radio} value="dragon">Dragon</Radio>
                    </RadioGroup>
                  </div>
                  <Form>
                    <RadioGroup className={styles.radiogroup} data-testid="radio-group-example-2" isRequired>
                      <Label>Second Favorite pet</Label>
                      <Radio className={styles.radio} value="dogs" data-testid="radio-dog">Dog</Radio>
                      <Button>About dogs</Button>
                      <Radio className={styles.radio} value="cats">Cat</Radio>
                      <Button>About cats</Button>
                      <Radio className={styles.radio} value="dragon">Dragon</Radio>
                      <Button>About dragons</Button>
                      <FieldError className={styles.errorMessage} />
                    </RadioGroup>
                  </Form>
                  <Form>
                    <RadioGroup className={styles.radiogroup} data-testid="radio-group-example-3" defaultValue="dragon" isRequired>
                      <Label>Third Favorite pet</Label>
                      <Radio className={styles.radio} value="dogs" data-testid="radio-dog">Dog</Radio>
                      <Button>About dogs</Button>
                      <Radio className={styles.radio} value="cats">Cat</Radio>
                      <Button>About cats</Button>
                      <Radio className={styles.radio} value="dragon">Dragon</Radio>
                      <Button>About dragons</Button>
                      <FieldError className={styles.errorMessage} />
                    </RadioGroup>
                  </Form>
                </div>
                <div>
                  <Button onPress={close} style={{
                marginTop: 10
              }}>
                    Close
                  </Button>
                </div>
              </div>}
          </Dialog>
        </Modal>
      </ModalOverlay>
    </DialogTrigger>;
}`,...(D=(b=n.parameters)==null?void 0:b.docs)==null?void 0:D.source}}};var f,F,B;c.parameters={...c.parameters,docs:{...(f=c.parameters)==null?void 0:f.docs,source:{originalSource:`props => {
  return <Form>
      <RadioGroup {...props} className={styles.radiogroup} data-testid="radio-group-example" isRequired>
        <Label>Favorite pet</Label>
        <Radio className={styles.radio} value="dogs" data-testid="radio-dog">Dog</Radio>
        <Radio className={styles.radio} value="cats">Cat</Radio>
        <Radio className={styles.radio} value="dragon">Dragon</Radio>
        <FieldError className={styles.errorMessage} />
      </RadioGroup>
      <Button type="submit">Submit</Button>
      <Button type="reset">Reset</Button>
    </Form>;
}`,...(B=(F=c.parameters)==null?void 0:F.docs)==null?void 0:B.source}}};const V=["RadioGroupExample","RadioGroupControlledExample","RadioGroupInDialogExample","RadioGroupSubmitExample"];export{l as RadioGroupControlledExample,u as RadioGroupExample,n as RadioGroupInDialogExample,c as RadioGroupSubmitExample,V as __namedExportsOrder,P as default};
