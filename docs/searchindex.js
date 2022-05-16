Search.setIndex({docnames:["app","index","modules"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["app.rst","index.rst","modules.rst"],objects:{"":[[0,0,0,"-","app"]],"app.forms":[[0,2,1,"","CartForm"],[0,2,1,"","CheckoutForm"],[0,2,1,"","DeleteAccountForm"],[0,2,1,"","FillOrderForm"],[0,2,1,"","LoginForm"],[0,2,1,"","NewDiscountForm"],[0,2,1,"","NewPercentageDiscountForm"],[0,2,1,"","NewProductForm"],[0,2,1,"","PasswordForm"],[0,2,1,"","RegisterForm"],[0,2,1,"","ReviewForm"]],"app.forms.CartForm":[[0,3,1,"","product_id"],[0,3,1,"","quantity"],[0,3,1,"","submit"]],"app.forms.CheckoutForm":[[0,3,1,"","address"],[0,3,1,"","billing"],[0,3,1,"","discount_code"],[0,3,1,"","submit"]],"app.forms.DeleteAccountForm":[[0,3,1,"","confirm"],[0,3,1,"","submit"]],"app.forms.FillOrderForm":[[0,3,1,"","merchant_id"],[0,3,1,"","order_id"],[0,3,1,"","submit"]],"app.forms.LoginForm":[[0,3,1,"","password"],[0,3,1,"","submit"],[0,3,1,"","username"]],"app.forms.NewDiscountForm":[[0,3,1,"","amount"],[0,3,1,"","code"],[0,3,1,"","expiration_date"],[0,3,1,"","products"],[0,3,1,"","submit"]],"app.forms.NewPercentageDiscountForm":[[0,3,1,"","amount"],[0,3,1,"","code"],[0,3,1,"","expiration_date"],[0,3,1,"","products"],[0,3,1,"","submit"]],"app.forms.NewProductForm":[[0,3,1,"","category"],[0,3,1,"","description"],[0,3,1,"","merchant_id"],[0,3,1,"","name"],[0,3,1,"","pictures"],[0,3,1,"","price"],[0,3,1,"","submit"]],"app.forms.PasswordForm":[[0,3,1,"","new_password"],[0,3,1,"","new_password_repeat"],[0,3,1,"","original_password"],[0,3,1,"","submit"]],"app.forms.RegisterForm":[[0,3,1,"","email"],[0,3,1,"","password"],[0,3,1,"","submit"],[0,3,1,"","username"]],"app.forms.ReviewForm":[[0,3,1,"","body"],[0,3,1,"","rating"],[0,3,1,"","submit"]],"app.models":[[0,2,1,"","CartItem"],[0,2,1,"","Category"],[0,2,1,"","Discount"],[0,2,1,"","Image"],[0,2,1,"","Order"],[0,2,1,"","OrderRow"],[0,2,1,"","Product"],[0,2,1,"","Review"],[0,2,1,"","Role"],[0,2,1,"","User"],[0,5,1,"","load_user"]],"app.models.CartItem":[[0,3,1,"","id"],[0,3,1,"","product_id"],[0,3,1,"","quantity"],[0,3,1,"","timestamp"],[0,3,1,"","user_id"]],"app.models.Category":[[0,3,1,"","id"],[0,3,1,"","name"],[0,3,1,"","products"]],"app.models.Discount":[[0,4,1,"","apply_discount"],[0,3,1,"","code"],[0,3,1,"","details"],[0,3,1,"","expiration"],[0,3,1,"","id"],[0,4,1,"","is_valid"]],"app.models.Image":[[0,3,1,"","id"],[0,3,1,"","path"],[0,3,1,"","product"],[0,3,1,"","product_id"]],"app.models.Order":[[0,3,1,"","id"],[0,3,1,"","order_row"],[0,3,1,"","ship_address"],[0,3,1,"","user"],[0,3,1,"","user_id"]],"app.models.OrderRow":[[0,3,1,"","filled"],[0,3,1,"","id"],[0,3,1,"","order"],[0,3,1,"","product"],[0,3,1,"","product_id"],[0,3,1,"","product_price"],[0,3,1,"","quantity"],[0,3,1,"","row_id"],[0,3,1,"","timestamp"]],"app.models.Product":[[0,3,1,"","category"],[0,3,1,"","category_id"],[0,3,1,"","description"],[0,3,1,"","id"],[0,3,1,"","images"],[0,3,1,"","merchant_id"],[0,3,1,"","name"],[0,3,1,"","orders"],[0,3,1,"","price"],[0,3,1,"","reviews"],[0,3,1,"","user"]],"app.models.Review":[[0,3,1,"","body"],[0,3,1,"","id"],[0,3,1,"","product"],[0,3,1,"","product_id"],[0,3,1,"","rating"],[0,3,1,"","timestamp"],[0,3,1,"","user_id"]],"app.models.Role":[[0,3,1,"","id"],[0,3,1,"","name"]],"app.models.User":[[0,3,1,"","cart_items"],[0,4,1,"","check_password"],[0,3,1,"","email"],[0,3,1,"","id"],[0,3,1,"","orders"],[0,3,1,"","password_hash"],[0,3,1,"","products"],[0,3,1,"","roles"],[0,4,1,"","set_password"],[0,3,1,"","username"]],"app.routes":[[0,5,1,"","account_info"],[0,5,1,"","account_test"],[0,5,1,"","add_categories"],[0,5,1,"","admin_promo"],[0,5,1,"","admin_promo_percentage"],[0,5,1,"","cart"],[0,5,1,"","cart_remove"],[0,5,1,"","category"],[0,5,1,"","checkout"],[0,5,1,"","delete_account"],[0,5,1,"","discounts"],[0,5,1,"","home"],[0,5,1,"","images"],[0,5,1,"","login"],[0,5,1,"","logout"],[0,5,1,"","merchant"],[0,5,1,"","merchant_account_test"],[0,5,1,"","merchant_login"],[0,5,1,"","merchant_new_product"],[0,5,1,"","merchant_orders"],[0,5,1,"","merchant_orders_filled"],[0,5,1,"","merchant_profile"],[0,5,1,"","merchant_promo"],[0,5,1,"","merchant_promo_percentage"],[0,5,1,"","merchant_register"],[0,5,1,"","orders"],[0,5,1,"","orders_filled"],[0,5,1,"","product"],[0,5,1,"","product_page"],[0,5,1,"","product_review"],[0,5,1,"","register"],[0,5,1,"","render_template"],[0,5,1,"","search"]],"app.utils":[[0,5,1,"","admin_required"],[0,5,1,"","create_discount"],[0,5,1,"","get_admin"],[0,5,1,"","get_categories"],[0,5,1,"","get_category_dict"],[0,5,1,"","get_merchant"],[0,5,1,"","is_merchant"],[0,5,1,"","merchant_required"],[0,5,1,"","prevent_merchant"]],app:[[0,1,1,"","db"],[0,0,0,"-","forms"],[0,0,0,"-","models"],[0,0,0,"-","routes"],[0,0,0,"-","utils"],[0,1,1,"","webapp"]]},objnames:{"0":["py","module","Python module"],"1":["py","data","Python data"],"2":["py","class","Python class"],"3":["py","attribute","Python attribute"],"4":["py","method","Python method"],"5":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:data","2":"py:class","3":"py:attribute","4":"py:method","5":"py:function"},terms:{"0":[0,1],"1":[0,1],"10":0,"127":1,"131_project":[0,1],"2":0,"3":[0,1],"4":0,"404":0,"5":0,"5000":1,"6":0,"7":0,"8":[0,1],"9":0,"boolean":0,"class":0,"default":0,"float":0,"function":0,"int":0,"new":0,"return":0,"true":0,"try":1,A:0,If:1,The:0,Will:0,abl:0,abort:0,about:0,accept:0,access:[0,1],account:0,account_info:0,account_test:0,action:0,add:0,add_categori:0,address:0,admin:0,admin_promo:0,admin_promo_percentag:0,admin_requir:0,after:0,against:0,all:0,allow:0,alreadi:0,also:0,amount:0,an:0,app:1,appli:0,applic:0,applicable_id:0,apply_discount:0,arg:0,attribut:0,automat:0,back:0,base:0,befor:0,belong:0,bill:0,bodi:0,bool:0,booleanfield:0,browser:1,can:0,card:0,cart:0,cart_item:0,cart_remov:0,cartform:0,cartitem:0,catalog:0,categori:0,category_id:0,categorywid:0,cd:1,chang:0,check:0,check_password:0,checkout:0,checkoutform:0,choic:0,clone:1,code:0,com:1,commerc:1,compar:0,complet:0,confirm:0,connect:[0,1],construct:0,contain:0,content:2,correct:0,creat:[0,1],create_db:1,create_discount:0,credit:0,current:0,current_us:0,custom:[0,1],databas:[0,1],datarequir:0,date:0,datefield:0,datetim:0,db:0,decl_api:0,decor:0,delet:0,delete_account:0,deleteaccountform:0,descript:0,detail:0,dictionari:0,discount:0,discount_cod:0,document:0,download:1,dropdown:0,each:0,edit:0,els:0,email:0,end:0,end_dat:0,engin:0,error:1,expir:0,expiration_d:0,fals:0,fetch:0,field:0,file:[0,1],fileallow:0,filenam:0,fill:0,fillorderform:0,fix:0,flask:[0,1],flask_login:0,flask_wtf:0,flaskform:0,flasklogin:0,floatfield:0,folder:1,foreign:0,form:[1,2],found:0,from:[0,1],func:0,g:1,gener:0,get:0,get_admin:0,get_categori:0,get_category_dict:0,get_merch:0,git:1,github:1,give:0,given:0,ha:0,handl:0,hash:0,have:0,haven:0,hidden:0,hiddenfield:0,home:0,http:1,i:0,id:0,imag:0,index:1,info:0,inform:0,input:0,instanc:0,instrumentedlist:0,is_merch:0,is_valid:0,item:0,jinja:1,jpeg:0,jpg:0,json:0,kei:0,kwarg:0,librari:1,link:0,list:0,load_us:0,loader:0,local:1,localhost:1,log:0,login:0,loginform:0,logout:0,machin:1,make:1,manual:1,match:0,merchant:[0,1],merchant_account_test:0,merchant_id:0,merchant_login:0,merchant_new_product:0,merchant_ord:0,merchant_orders_fil:0,merchant_profil:0,merchant_promo:0,merchant_promo_percentag:0,merchant_regist:0,merchant_requir:0,method:0,mixin:0,model:[1,2],modul:[1,2],multi:0,multipl:0,multiplefilefield:0,my:0,name:0,nathancye:1,nathanye:0,navig:1,new_password:0,new_password_repeat:0,newdiscountform:0,newpercentagediscountform:0,newproductform:0,non:0,number:0,numberrang:0,numer:0,object:0,occur:1,onc:0,onli:0,option:0,order:0,order_id:0,order_row:0,orderrow:0,orders_fil:0,origin:0,original_password:0,orm:0,otherwis:0,out:0,packag:[1,2],page:[0,1],param:0,paramet:0,password:0,password_hash:0,passwordfield:0,passwordform:0,path:0,percentag:0,pictur:0,pip:1,place:0,pleas:1,png:0,post:0,prerequisit:1,prevent:0,prevent_merch:0,price:0,primari:0,process:0,prod_id:0,product:0,product_id:0,product_pag:0,product_pric:0,product_review:0,project:1,promot:0,purchas:0,py:1,python3:1,python:[0,1],q:0,quantiti:0,queri:0,queryabl:0,rate:0,reachabl:0,receiv:0,reciev:0,redirect:0,regex:0,regist:0,registerform:0,registr:0,relat:0,relationship:0,remov:0,render_templ:0,repeat:0,repres:0,request:0,requir:0,reset:0,result:0,retriev:0,review:0,reviewform:0,revolutionari:1,role:0,rout:[1,2],row:0,row_id:0,run:[0,1],s:0,save:0,search:[0,1],see:0,select:0,selectfield:0,selectmultiplefield:0,set:0,set_password:0,ship:0,ship_address:0,should:0,site:[0,1],sitewid:0,sourc:0,specif:0,sqlalchemi:0,sqlite:0,statu:0,still:0,store:[0,1],str:0,string:0,stringfield:0,submit:0,submitfield:0,submitt:0,submodul:[1,2],support:0,sure:1,t:0,take:0,test:0,text:0,textareafield:0,thei:0,through:0,time:0,timestamp:0,type:0,unboundfield:0,unfil:0,upgrad:1,upload:0,us:[0,1],usd:[],user:0,user_id:0,usermixin:0,usernam:0,utcnow:0,util:[1,2],valid:0,valu:0,verifi:0,wa:0,want:0,warn:0,web:0,webapp:[0,1],webp:0,webpag:0,websit:[0,1],well:0,when:0,which:[0,1],work:1,would:0,written:0,wtform:0,zip:1},titles:["app package","Welcome to E-Buy\u2019s documentation!","app"],titleterms:{app:[0,2],bui:1,content:[0,1],document:1,e:1,form:0,indic:1,instal:1,model:0,modul:0,packag:0,rout:0,s:1,setup:1,submodul:0,tabl:1,util:0,welcom:1}})