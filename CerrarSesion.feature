@Popups
Feature: Popups de finalizacion de sesion


    @PopupCerrarSesion @CLOSE_SESSION1
    Scenario Outline: [HAPPY PATH] Usuario espera primer popup y dar click en cerrar sesion
      Given que el usuario esta en iframe de iniciar sesion de benefit
      And selecciona la opcion inicia sesion
      And el selecciona el tipo de documento DNI e ingresa numero de documento 54872045 y contrasena Lima12345$
      And el presiona el boton ingresar
      And validamos que se muestra cintillo
      And abrimos el link de la pagina <ruta>
      When esperamos a que se muestre popup y damos click en cerrar sesion
      Then validamos que nos redirecciona al home de benefit deslogueados


      Examples:
        | ruta                |
        | https://saaspp.com/productos/cuidado-corporal   |

