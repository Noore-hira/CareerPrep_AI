import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  RiCloseLine,
  RiEyeLine,
  RiEyeOffLine,
  RiSaveLine,
} from "react-icons/ri";


const MODELS = [
  "llama-3.1-8b-instant",
  "llama-3.3-70b-versatile",
  "meta-llama/llama-4-scout-17b-16e-instruct",
];


interface SettingsSidebarProps {

  open: boolean;

  onClose: () => void;

}



export default function SettingsSidebar({

  open,

  onClose,

}: SettingsSidebarProps) {


  const [apiKey, setApiKey] = useState("");

  const [model, setModel] =
    useState(MODELS[1]);

  const [remember, setRemember] =
    useState(true);

  const [showKey, setShowKey] =
    useState(false);



  useEffect(() => {


    const savedKey =
      localStorage.getItem(
        "groq_api_key"
      );


    const savedModel =
      localStorage.getItem(
        "groq_model"
      );



    if(savedKey){

      setApiKey(savedKey);

      setRemember(true);

    }



    if(savedModel){

      setModel(savedModel);

    }



  },[]);




  const handleApiKeyChange = (
    value:string
  )=>{


    setApiKey(value);


    // keep localStorage updated
    if(remember){

      localStorage.setItem(
        "groq_api_key",
        value.trim()
      );

    }


  };




  const handleModelChange = (
    value:string
  )=>{


    setModel(value);


    localStorage.setItem(
      "groq_model",
      value
    );


  };





  const saveSettings = ()=>{


    if(!apiKey.trim()){


      alert(
        "Please enter your Groq API Key."
      );

      return;

    }




    if(remember){


      localStorage.setItem(
        "groq_api_key",
        apiKey.trim()
      );


    }

    else{


      localStorage.removeItem(
        "groq_api_key"
      );


    }



    localStorage.setItem(
      "groq_model",
      model
    );



    console.log(
      "Saved API Key:",
      apiKey.substring(0,10)+"..."
    );


    alert(
      "Settings saved successfully."
    );


    onClose();


  };





  return (

    <AnimatePresence>


      {open && (

        <>


          <motion.div

            initial={{opacity:0}}

            animate={{opacity:0.45}}

            exit={{opacity:0}}

            className="fixed inset-0 bg-black z-40"

            onClick={onClose}

          />




          <motion.div


            initial={{x:-420}}

            animate={{x:0}}

            exit={{x:-420}}


            transition={{
              duration:0.25
            }}


            className="
              fixed
              left-0
              top-0
              h-screen
              w-96
              bg-[#10131a]
              border-r
              border-white/10
              shadow-2xl
              z-50
              p-8
            "

          >



            <div className="flex justify-between items-center mb-8">


              <h2 className="text-xl font-bold text-white">

                Groq Settings

              </h2>



              <button onClick={onClose}>

                <RiCloseLine className="text-2xl text-gray-400 hover:text-white"/>

              </button>


            </div>




            <label className="block text-sm text-gray-300 mb-2">

              Groq API Key

            </label>



            <div className="relative mb-6">


              <input


                type={
                  showKey
                  ? "text"
                  : "password"
                }


                value={apiKey}


                onChange={(e)=>
                  handleApiKeyChange(
                    e.target.value
                  )
                }


                placeholder="gsk_xxxxxxxxx"


                className="
                  w-full
                  rounded-xl
                  bg-[#181c24]
                  border
                  border-white/10
                  px-4
                  py-3
                  text-white
                  outline-none
                  focus:border-violet-500
                "


              />



              <button

                type="button"

                onClick={()=>
                  setShowKey(!showKey)
                }

                className="
                  absolute
                  right-4
                  top-3.5
                  text-gray-400
                "

              >

                {
                  showKey
                  ?
                  <RiEyeOffLine/>
                  :
                  <RiEyeLine/>
                }


              </button>


            </div>





            <label className="block text-sm text-gray-300 mb-2">

              Model

            </label>




            <select


              value={model}


              onChange={(e)=>
                handleModelChange(
                  e.target.value
                )
              }


              className="
                w-full
                rounded-xl
                bg-[#181c24]
                border
                border-white/10
                px-4
                py-3
                text-white
                mb-6
              "


            >

              {
                MODELS.map((m)=>(

                  <option
                    key={m}
                    value={m}
                  >

                    {m}

                  </option>

                ))
              }


            </select>





            <label className="flex items-center gap-3 mb-8 cursor-pointer">


              <input

                type="checkbox"

                checked={remember}

                onChange={()=>
                  setRemember(!remember)
                }

              />


              <span className="text-gray-300">

                Remember API Key

              </span>


            </label>





            <button


              onClick={saveSettings}


              className="
                w-full
                flex
                items-center
                justify-center
                gap-2
                rounded-xl
                bg-violet-600
                hover:bg-violet-700
                py-3
                text-white
                font-semibold
              "


            >

              <RiSaveLine/>

              Save Settings


            </button>




          </motion.div>


        </>

      )}


    </AnimatePresence>

  );

}