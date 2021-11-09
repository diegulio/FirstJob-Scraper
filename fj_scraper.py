# -*- coding: utf-8 -*-
import re

# Selenium desde google colab (Webdriver)
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()


# Ignoro Deprecation warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore")

wd = webdriver.Chrome(options= chrome_options, executable_path = '/Users/diegulio/Desktop/FJ-Scraper/chromedriver')


def get_company(job):
    '''
    Función que extrae la compañia del trabajo

    Parameters
    ----------
    job : Elemento html 
        Trabajo.

    Returns
    -------
    company : str
        Compañia a la cual pertenece el trabajo.

    '''
    
    info = job.find_element_by_tag_name('h5').text
    company = re.search(r'(.*),', info).group(1) # Extraigo todo lo que está antes de la coma excluyendola
    return company

def get_type(job):
    '''
    Función que extrae el tipo de la publicación.
    (trabajo o práctica)

    Parameters
    ----------
    job : Elemento html 
        Trabajo.

    Returns
    -------
    type_ : str
        tipo de trabajo a la cual pertenece el trabajo.

    '''
    
    type_ = job.find_element_by_class_name('label-fj-type').text
    return type_
  
def get_link(job):
    '''
    Función que extrae el link del trabajo

    Parameters
    ----------
    job : Elemento html 
        Trabajo.

    Returns
    -------
    link : str
        link del trabajo

    '''
    a = job.find_element_by_tag_name('a')
    link = a.get_attribute('href')
    return link

def fill_form(driver, position_element):
    '''
    Función que rellena el formulario con la data

    Parameters
    ----------
    driver : TYPE
        Driver Navegador.
    position_element : str
        Palabra clave a buscar.

    Returns
    -------
    driver : TYPE
        Driver de navegador con el formulario rellenado.

    '''
    driver.find_element_by_id("title").send_keys(position_element) # relleno el text box 'Buscar por nombre del cargo: {position_element}'
    driver.find_element_by_id("filter_type_work_1").click() # Checkeo el Check-box de prácticas
    driver.find_element_by_tag_name('button').click() # Clickeo botón submit
    return driver

def reset_form(driver, url):
    '''
    Función que resetea el drive a la página principal

    Parameters
    ----------
    driver : TYPE
        Driver del navegador.
    url : TYPE
        Url a la cual se reiniciará.

    Returns
    -------
    driver : TYPE
        Nuevo driver seteado en el url.

    '''
    
    fj_url = url
    driver.get(fj_url)
    return driver


  
def get_time(job):
    '''
    Función que extrae el el tiempo  de la publicación
    de trabajo

    Parameters
    ----------
    job : Elemento html 
        Trabajo.

    Returns
    -------
    num : int
        numero de el tiempo
    time : str
        tiempo (hora, dias, meses,etc)

    '''
    info = job.find_element_by_tag_name('h5').text
    # retornare una lista con un numero y un tiempo ej: [2,dias] -> publicada hace 2 dias
    num = re.search(r'\s(\d*)\s', info).group(1)
    time = re.search(r'\d\s(\w*)', info).group(1)
    return (num,time)

def get_title(job):
    '''
    Función que extrae el titulo del trabajo

    Parameters
    ----------
    job : Elemento html 
        Trabajo.

    Returns
    -------
    title : str
        titulo del trabajo

    '''
    title = job.find_element_by_tag_name('h4').text
    return title

def get_jobs(driver):
    '''
    Función que obtiene todas las publicaciones de trabajo y muestra info.
    Esta las identifico ya que se encuentran en elementos html 
    de clase col-xs-12

    Parameters
    ----------
    driver : TYPE
        Driver del navegador.

    Returns
    -------
    None.

    '''
    
    # Trabajos que aparecen en la página principal
    jobs = driver.find_elements_by_class_name('col-xs-12')
    for job in jobs:
      try:
        head = job.find_element_by_class_name('hgroup')
        print(head.find_element_by_tag_name('h4').text)
        print(head.find_element_by_tag_name('h5').text)
        print(get_company(job))
        print(get_type(job))
        print(get_link(job))
        print(get_time(job))
        print(get_title(job))
        print('-----')
      except:
        pass


class internship():
    # Clase de práctica
    
    def __init__(self, title, company, type_, link, time):
      self.title = title
      self.company = company
      self.type_ = type_
      self.link = link
      self.time = time




# Realizar conexión
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

fj_url = 'https://firstjob.me/ofertas'
wd.get(fj_url)

def recommendation(interest_areas):
  '''
  Función que entrega las recomendaciones de todas las áreas de interés deseadas

  Args:
  ------
  * interest_areas: Áreas de interés del usuario. List

  Outputs:
  ---------
  * recommends: Diccionario con áreas como keys y una lista de objetos de prácticas
  como values. Dict

  * jobs_count: Contador de trabajos recomendados. Int
  '''

  # Conexión al driver
  wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

  # Se fija Url First Job Ofertas
  fj_url = 'https://firstjob.me/ofertas'
  wd.get(fj_url)


  recommends = {} # Diccionario de recomendaciones finales
  recommended_links = [] # Todos los links de las prácticas escogidas (esto se usa
              # para descartar duplicados)
  jobs_count = 0 # contador de practicas encontradas

  for area in interest_areas:
    # Se rellena el formulario con el area
    form_driver = fill_form(wd, area) 

    internships = [] # practicas del area
    jobs = form_driver.find_elements_by_class_name('col-xs-12') # Los trabajos vienen con esta clase

    for job in jobs:
      try: # Probamos, porque no todos son trabajos
        title = get_title(job) # titulo
        company = get_company(job) # empresa
        type_ = get_type(job) # trabajo o práctica
        link = get_link(job) # link
        num_time,time = get_time(job)  # [numero, tiempo] e.g [3, días]
    

        # Se supone que todas son prácticas ya que se
        # indicó en el formulario

        # Se analiza el tiempo, sólo me interesará aquellas publicadas en 'horas' 
        # o 'día' (en first job 'día' -> 1 día, cuando son más le ponen 'días')
        
        
        if time in ['horas', 'día']:
          if link not in recommended_links: # si aún no se ha recomendado el link

            # Se crea objeto practica con sus datos
            inship = internship(title, company, type_, link, (num_time,time))
            # Se agrega a las practicas del área
            internships.append(inship) 
            # Lo agrego a la lista global de links 
            # para descartar duplicados
            recommended_links.append(link) 
                          
            jobs_count += 1
      except: # Si no es un trabajo
        pass # no se hace nada
      
      
    # Se agregan practicas a las recomendaciones
    recommends[area] = internships 
    # Se resetea el form(driver)
    wd = reset_form(wd, fj_url)

  return recommends, jobs_count



# Prueba

interest_areas = ['data', 'supply', '']
rec, count = recommendation(interest_areas)





