"""Asumo que la siguiente aplicación está pensada para los trabajadores del cine y no para compras online ya que no todos deberían poder 
agregar asientos libremente o aplicar descuentos introduciendo su edad sin demostrar un documento acreditativo. Adicionalmente,
para evitar errores ya que no se habla de una aplicación para diferentes días, se asume que tanto la reserva como la operación de 
mostrar asientos funciona para la fecha/día actual."""

from datetime import datetime

class Asiento:
    def __init__(self, numero, fila):
        #Primero nos aseguramos que el número introducido tanto para el número de asiento como para fila son enteros mayores de 0.
        if not isinstance(numero, int) or numero <= 0:
            raise ValueError("El número de asiento debe ser un entero positivo.")
        if not isinstance(fila, int) or fila <= 0:
            raise ValueError("La fila del asiento debe ser un entero positivo.")
        self.__numero = numero
        self.__fila = fila
        self.__reservado = False
        self.__precio = 0
    
    def get_numero(self):
        return self.__numero #devuelve el valor de la variable numero
    
    def get_fila(self):
        return self.__fila #devuelve el valor de la variable fila
    
    def is_reservado(self):
        return self.__reservado #devuelve un valor boolean dependiendo si el asiento está reservado o no
    
    def set_reservado(self, reservado):
        self.__reservado = reservado #cambia el estado de asiento reservado a True/False
    
    def get_precio(self):
        return self.__precio #devuelve el valor de la variable precio
    
    def set_precio(self, precio):
        self.__precio = precio #asigna valor a la variable precio


class SalaCine:
    def __init__(self, filas, asientos_por_fila):
        #Primero nos aseguramos que el número introducido tanto para el número de asientos por fila como para el número total de filas #
        #son enteros mayores de 0.#
        if not isinstance(asientos_por_fila, int) or asientos_por_fila <= 0:
            raise ValueError("El número de asientos en cada fila debe ser un entero positivo.")
        if not isinstance(filas, int) or filas <= 0:
            raise ValueError("El número total de filas debe ser un entero positivo.")

        #Construimos una lista que va a contener todos los asientos en todas las filas que hay en la sala de cine
        self.__asientos = []
        for fila in range(1, filas + 1):
            for numero in range(1, asientos_por_fila + 1):
                self.__asientos.append(Asiento(numero, fila))
    
    #Creamos un getter para obtener el número de filas en la sala
    def get_filas(self):
        return len(set([asiento.get_fila() for asiento in self.__asientos]))
    
    #Creamos un getter para obtener el número de asientos en cada fila en la sala
    def get_asientos_por_fila(self):
        return len(set([asiento.get_numero() for asiento in self.__asientos]))
          
    def reservar_asiento(self, numero, fila, edad, dia_semana=datetime.today().weekday(), precio_base=10): #precio base por defecto: 10€
        #Para que el descuento se aplique automáticamente si el día es un miércoles, cogemos el día actual usando la #
        #biblioteca datetime
        asiento = self.buscar_asiento(numero, fila)
        if asiento:
            if asiento.is_reservado() == False:
                precio = precio_base
                if dia_semana == 2: #miercoles
                    precio *= 0.8
                if edad > 65:
                    precio *= 0.7
                asiento.set_precio(precio)
                asiento.set_reservado(True)
                return f"Asiento {numero} en fila {fila} ha sido reservado. Precio: {precio:.2f}€"
            else:
                raise ValueError("El asiento ya está reservado.")
        else:
            raise ValueError("El asiento no existe.")

    
    def cancelar_reserva(self, numero, fila):
        asiento = self.buscar_asiento(numero, fila)
        if asiento:
            if asiento.is_reservado():
                asiento.set_reservado(False)
                asiento.set_precio(0)
                return f"Reserva del asiento {numero} en fila {fila} ha sido cancelada."
            else:
                raise ValueError("El asiento no está reservado.")
        else:
            raise ValueError("El asiento no existe.")


    def agregar_asiento(self, asiento):
        #Verificar si ya existe un asiento así
        for a in self.__asientos:
            if a.get_numero() == asiento.get_numero() and a.get_fila() == asiento.get_fila():
                raise ValueError("El asiento ya está registrado en la sala.")
            
        """Obtener número de asientos por fila. Se decide dejar la posibilidad de agregar asientos solamente en filas ya existentes
         y como continuación de una fila."""
        if self.__asientos:
            ultima_fila = self.__asientos[-1].get_fila()
            if asiento.get_fila() > ultima_fila:
                raise ValueError(f"El número de fila es mayor que el número total de filas en la sala. No se permite crear nuevas" 
                                 f" filas. Se puede agregar asientos en filas de {self.__asientos[0].get_fila()} a {ultima_fila}.")
            ultimo_numero = self.__asientos[-1].get_numero()
            if asiento.get_numero() != ultimo_numero + 1:
                raise ValueError(f"El número del asiento no es el siguiente en la fila. Sólo se permite agregar asientos en orden. "
                                 f"El número del siguiente asiento disponible es: {ultimo_numero + 1}.")
        
        #Insertar el asiento en la posición correcta en la lista de asientos
        posicion = 0
        for a in self.__asientos:
            if asiento.get_fila() < a.get_fila() or (
                asiento.get_fila() == a.get_fila() and asiento.get_numero() < a.get_numero()):
                break
            posicion += 1
        
        self.__asientos.insert(posicion, asiento)
        return f"Asiento {asiento.get_numero()} en fila {asiento.get_fila()} ha sido agregado."


    def mostrar_asientos(self, dia_semana=datetime.today().weekday(), precio_base=10):
        #Creamos una lista de todos los asientos para mostrar su disponibilidad y precio
        todos_asientos = []
        if dia_semana == 2: #miercoles
            precio_base *= 0.8
        for asiento in self.__asientos:
            estado = "Reservado" if asiento.is_reservado() else "Disponible"
            if asiento.is_reservado():
                precio = asiento.get_precio()
            else:
                precio = precio_base
            todos_asientos.append(f"Asiento {asiento.get_numero()}, fila {asiento.get_fila()}: {estado}, Precio: {precio}€")
        return "\n".join(todos_asientos)
    
    def buscar_asiento(self, numero, fila):
        for asiento in self.__asientos:
            if asiento.get_numero() == numero and asiento.get_fila() == fila:
                return asiento
        return None


#Ejemplos de uso
if __name__ == "__main__":
    #Primero creamos una sala de cine con filas y asientos por fila según nuestro criterio
    sala = SalaCine(filas=7, asientos_por_fila=10)

    #Ver todos los asientos disponibles en la sala creada con su precio correspondiente dependiendo del día
    print(sala.mostrar_asientos())

    '''Reservar el asiento elegido por el trabajador. Para eso pedimos que introduzca el número de asiento, 
    el número de fila y la edad del cliente que tiene que ser un valor entero positivo y menor de 110.'''
    while True:
        try:
            numero_fila = int(input("Introduce el número de la fila donde quiere reservar el asiento: "))
            numero_asiento = int(input("Introduce el número de asiento que quiere reservar en esa fila: "))
            edad_cliente = int(input("Introduce edad del cliente: "))

            # Validación de entrada
            if not 1 <= numero_asiento <= sala.get_asientos_por_fila():
                raise ValueError("Número de asiento incorrecto.")
            if not 1 <= numero_fila <= sala.get_filas():
                raise ValueError("Número de fila incorrecto.")
            if not 0 <= edad_cliente <= 110:  # Rango de edad razonable
                raise ValueError("Edad incorrecta.")

            print(sala.reservar_asiento(numero=numero_asiento, fila=numero_fila, edad=edad_cliente))

            # Opción para reservar otro asiento
            continuar = input("¿Quieres reservar otro asiento? (s/n): ")
            if continuar.lower() != 's':
                break

        except ValueError as e:
            print(f"Error: {e}")


    #Mostrar asientos después de la reserva
    print(sala.mostrar_asientos())
    
    #Agregar un asiento específico
    #print(sala.agregar_asiento(Asiento(numero=11, fila=3)))

    #Mostrar asientos después de añadir el asiento
    #print(sala.mostrar_asientos())

    #Cancelar reserva de un asiento específico o el mismo que se acaba de reservar
    #print(sala.cancelar_reserva(numero=numero_asiento, fila=numero_fila))
