# lgpd
Code to scan all files in a directory to look for sensitive data according to LGPD directions.


# How to use

1.  Clone or download the repository in the **master branch** (change it on top left. you are on the main branch now). Clone by clicking on the green buttom on the right!
2.  Create a virtual environment to install all the necessary packages (see https://docs.python.org/3/library/venv.html)
3.  Activate you VENV
4.  Install all packages with:
           
           pip install -r requirements.txt
     
5.  From the cm, run the main file with the root directory you want to scan:

          python -m main C:/Users/youruser/Documents
          
 6. The output will be saved in the same folder you run the code.
 
 7. In the output there will be a columns for each of the target data types (see below) and one called __sensitive__ that says if there is any of the target data in the document following the legend:
              
                0 -> no data found.
                1 -> data matches patterns BUT there is no keyword associated. ex: __2344-6285 for telephone__
                2 -> data matches patterns AND there is keyword associated. ex: __telefone 2344-6285__
 
 
 OBS: The rules can be found in **Searchers.py**
      The script is looking for the following data:
      
            - cpf
            - rg
            - cep
            - data de nascimento
            - nome
            - telefone
            - email
      
      
  __WIP__
