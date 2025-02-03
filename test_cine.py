import unittest
from cine import Asiento, SalaCine

class PruebasSistemaReservas(unittest.TestCase):

    def setUp(self):
        #Configuración inicial para los tests
        self.sala = SalaCine(filas=5, asientos_por_fila=10)
    
    def test_validar_asiento(self):
        #Test para validar si se puede agrega un asiento permitido
        asiento = Asiento(numero=11, fila=3)
        try:
            self.sala.agregar_asiento(asiento)
        except ValueError:
            self.fail("Se generó una excepción ValueError.")
    
    def test_validar_asiento_invalido(self):
        #Test para validar un numero de asiento o fila inválida
        with self.assertRaises(ValueError):
            asiento = Asiento(numero=12, fila=3) #Asiento fuera de rango aceptable
            self.sala.agregar_asiento(asiento)
    
    def test_validar_edad_correcta(self):
        #Test para validar si la edad tiene derecho a descuento
        self.sala.reservar_asiento(numero=5, fila=3, edad=80, dia_semana=1)
        asiento = self.sala.buscar_asiento(numero=5, fila=3)
        self.assertLess(asiento.get_precio(), 10) #Comprobar si el precio es menor que 10
    
    def test_validar_edad_incorrecta(self):
        #No se espera una excepción pero el descuento no se debería aplicar
        self.sala.reservar_asiento(numero=5, fila=5, edad=40, dia_semana=5)
        asiento = self.sala.buscar_asiento(5, 5)
        self.assertEqual(asiento.get_precio(), 10) #Precio sin descuento

    def test_validar_dia_correcto(self):
        #Test para validar si el día es miércoles para aplicar descuento
        self.sala.reservar_asiento(numero=5, fila=3, edad=45, dia_semana=2)
        asiento = self.sala.buscar_asiento(numero=5, fila=3)
        self.assertLess(asiento.get_precio(), 10) #Comprobar si el precio es menor que 10
    
    def test_validar_dia_incorrecto(self):
        #No se espera una excepción pero el descuento no se debería aplicar
        self.sala.reservar_asiento(numero=5, fila=3, edad=25, dia_semana=3)
        asiento = self.sala.buscar_asiento(5, 3)
        self.assertEqual(asiento.get_precio(), 10) #Precio sin descuento
  
    def test_reservar_asiento_duplicado(self):
        #Test para manejar la excepción de reservar un asiento ya reservado
        self.sala.reservar_asiento(numero=5, fila=3, edad=25)
        with self.assertRaises(ValueError) as context:
            self.sala.reservar_asiento(numero=5, fila=3, edad=25)
        self.assertEqual(str(context.exception), "El asiento ya está reservado.")
    
    def test_cancelar_reserva_no_existente(self):
        #Test para manejar la excepción de cancelar una reserva noexistente
        with self.assertRaises(ValueError) as context:
            self.sala.cancelar_reserva(numero=7, fila=3)
        self.assertIn("El asiento no está reservado.", str(context.exception))


if __name__ == "__main__":
    unittest.main()
