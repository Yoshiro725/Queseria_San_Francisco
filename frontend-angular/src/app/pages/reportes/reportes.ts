import { Component, OnInit, Inject, PLATFORM_ID, ViewChild } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { ReporteSimulado } from '../../models/reporte-simulado.inteface';
import { BaseChartDirective } from 'ng2-charts';
import { 
  Chart, 
  registerables,
  ChartConfiguration,
  ChartType
} from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-reportes',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './reportes.html',
  styleUrl: './reportes.scss',
})
export class Reportes implements OnInit {
  
  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;
  
  public isBrowser: boolean;
  activeDateTab: string = 'dia';
  activeReportType: string = 'inventario';
  private reportesPorFecha: ReporteSimulado[] = [];
  public reportesFiltrados: ReporteSimulado[] = [];
  
  private datosDia: ReporteSimulado[] = [
    { fecha: '06/11/2025', tipo: 'Venta', descripcion: 'Venta a Supermercado El Buen Queso (20kg Queso Fresco)' },
    { fecha: '06/11/2025', tipo: 'Venta', descripcion: 'Venta a Cliente Menor (5kg Quesillo)' },
    { fecha: '06/11/2025', tipo: 'Venta', descripcion: 'Venta a Restaurante La Granja (10kg Queso Seco)' },
    { fecha: '06/11/2025', tipo: 'Venta', descripcion: 'Venta a Tienda Don Luis (8kg Crema)' },
    { fecha: '06/11/2025', tipo: 'Inventario', descripcion: 'Entrada de Queso Fresco (50kg)' },
    { fecha: '06/11/2025', tipo: 'Inventario', descripcion: 'Entrada de Yogurt (30kg)' }
  ];
  private datosSemana: ReporteSimulado[] = [
    { fecha: '06/11/2025', tipo: 'Venta', descripcion: 'Venta a Supermercado El Buen Queso (20kg Queso Fresco)' },
    { fecha: '06/11/2025', tipo: 'Venta', descripcion: 'Venta a Cliente Menor (5kg Quesillo)' },
    { fecha: '06/11/2025', tipo: 'Venta', descripcion: 'Venta a Restaurante La Granja (10kg Queso Seco)' },
    { fecha: '05/11/2025', tipo: 'Venta', descripcion: 'Venta a Tienda Don Luis (15kg Crema)' },
    { fecha: '05/11/2025', tipo: 'Venta', descripcion: 'Venta a Hotel Central (25kg Queso Fresco)' },
    { fecha: '04/11/2025', tipo: 'Inventario', descripcion: 'Entrada de Leche (Lechería Don Pepe - 200L)' },
    { fecha: '04/11/2025', tipo: 'Venta', descripcion: 'Venta a Mercado Principal (30kg Yogurt)' },
    { fecha: '03/11/2025', tipo: 'Venta', descripcion: 'Venta a Supermercado El Buen Queso (18kg Quesillo)' },
    { fecha: '03/11/2025', tipo: 'Venta', descripcion: 'Venta a Cliente Menor (12kg Crema)' }
  ];
  private datosMes: ReporteSimulado[] = [
    { fecha: '06/11/2025', tipo: 'Venta', descripcion: 'Venta a Supermercado El Buen Queso (20kg Queso Fresco)' },
    { fecha: '05/11/2025', tipo: 'Venta', descripcion: 'Venta a Tienda Don Luis (15kg Crema)' },
    { fecha: '05/11/2025', tipo: 'Venta', descripcion: 'Venta a Hotel Central (25kg Queso Fresco)' },
    { fecha: '04/11/2025', tipo: 'Inventario', descripcion: 'Entrada de Leche (Lechería Don Pepe - 200L)' },
    { fecha: '04/11/2025', tipo: 'Venta', descripcion: 'Venta a Mercado Principal (30kg Yogurt)' },
    { fecha: '03/11/2025', tipo: 'Venta', descripcion: 'Venta a Supermercado El Buen Queso (18kg Quesillo)' },
    { fecha: '02/11/2025', tipo: 'Inventario', descripcion: 'Compra de Sal y Cuajo (50kg Sal, 5L Cuajo)' },
    { fecha: '01/11/2025', tipo: 'Venta', descripcion: 'Venta grande (fin de mes - 100kg variados)' },
    { fecha: '31/10/2025', tipo: 'Inventario', descripcion: 'Entrada de Queso Seco (80kg)' },
    { fecha: '30/10/2025', tipo: 'Venta', descripcion: 'Venta a Cadena de Restaurantes (50kg Queso Seco)' },
    { fecha: '28/10/2025', tipo: 'Venta', descripcion: 'Venta a Supermercado Regional (45kg variados)' },
    { fecha: '25/10/2025', tipo: 'Inventario', descripcion: 'Compra de insumos (50kg Sal, 10L Cuajo)' },
    { fecha: '20/10/2025', tipo: 'Venta', descripcion: 'Venta a Exportación (200kg Queso Seco)' }
  ];
  private datosAnio: ReporteSimulado[] = [
    { fecha: '06/11/2025', tipo: 'Venta', descripcion: 'Venta a Supermercado El Buen Queso (20kg Queso Fresco)' },
    { fecha: '15/10/2025', tipo: 'Venta', descripcion: 'Venta grande octubre (120kg variados)' },
    { fecha: '10/10/2025', tipo: 'Inventario', descripcion: 'Entrada de Leche (500L - Lechería Don Pepe)' },
    { fecha: '01/09/2025', tipo: 'Venta', descripcion: 'Venta septiembre (150kg)' },
    { fecha: '15/08/2025', tipo: 'Venta', descripcion: 'Venta a Exportación (300kg Queso Seco)' },
    { fecha: '01/07/2025', tipo: 'Venta', descripcion: 'Venta julio (180kg variados)' },
    { fecha: '15/06/2025', tipo: 'Inventario', descripcion: 'Entrada junio (400L Leche)' },
    { fecha: '01/05/2025', tipo: 'Venta', descripcion: 'Venta mayo (200kg)' },
    { fecha: '15/04/2025', tipo: 'Venta', descripcion: 'Venta abril (160kg)' },
    { fecha: '01/03/2025', tipo: 'Venta', descripcion: 'Venta marzo (190kg)' },
    { fecha: '15/02/2025', tipo: 'Inventario', descripcion: 'Entrada febrero (450L Leche)' },
    { fecha: '01/01/2025', tipo: 'Venta', descripcion: 'Venta inicio de año (250kg variados)' }
  ];

  public barChartType: ChartType = 'bar';
  public barChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    scales: { y: { beginAtZero: true } }
  };
  public barChartLabels: string[] = ['Queso Fresco', 'Quesillo', 'Queso Seco', 'Crema', 'Yogurt'];
  public barChartData: ChartConfiguration['data'] = {
    labels: this.barChartLabels,
    datasets: [
      { 
        data: [50, 30, 15, 60, 45], 
        label: 'Inventario (Kg)', 
        backgroundColor: 'rgba(59, 130, 246, 0.5)', 
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1
      },
      { 
        data: [120, 150, 45, 80, 70], 
        label: 'Ventas ($)', 
        backgroundColor: 'rgba(34, 197, 94, 0.5)', 
        borderColor: 'rgba(34, 197, 94, 1)',
        borderWidth: 1,
        hidden: true 
      }
    ]
  };

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {
    this.isBrowser = isPlatformBrowser(this.platformId);
  }

  ngOnInit(): void {
    this.seleccionarDateTab(this.activeDateTab);
  }
  
  seleccionarDateTab(tab: string): void {
    this.activeDateTab = tab;
    switch (tab) {
      case 'dia': this.reportesPorFecha = this.datosDia; break;
      case 'semana': this.reportesPorFecha = this.datosSemana; break;
      case 'mes': this.reportesPorFecha = this.datosMes; break;
      case 'año': this.reportesPorFecha = this.datosAnio; break;
      default: this.reportesPorFecha = [];
    }
    this.filtrarReportes();
  }

  seleccionarReportType(tab: string): void {
    this.activeReportType = tab;
    this.filtrarReportes();
    
    if (tab === 'inventario') {
      if (this.barChartData.datasets) {
        this.barChartData.datasets[0].hidden = false;
        this.barChartData.datasets[1].hidden = true;
      }
    } else if (tab === 'ventas') {
      if (this.barChartData.datasets) {
        this.barChartData.datasets[0].hidden = true;
        this.barChartData.datasets[1].hidden = false;
      }
    }
  }
  
  filtrarReportes(): void {
    const tipoFiltro = this.activeReportType === 'inventario' ? 'Inventario' : 'Venta';
    this.reportesFiltrados = this.reportesPorFecha.filter(reporte => {
      return reporte.tipo === tipoFiltro;
    });
  }

  actualizarGraficaConDatos(): void {
    if (!this.isBrowser || !this.barChartData.datasets) return;

    // Contar cuántos registros hay en reportesFiltrados
    const cantidadRegistros = this.reportesFiltrados.length;
    
    // Distribuir los datos filtrados entre los productos de forma equitativa
    const datoPorProducto = cantidadRegistros > 0 ? Math.floor(cantidadRegistros / this.barChartLabels.length) : 0;
    const residuo = cantidadRegistros % this.barChartLabels.length;
    
    // Crear array con los datos distribuidos
    const datosDistribuidos = this.barChartLabels.map((_, index) => {
      return datoPorProducto + (index < residuo ? 1 : 0);
    });

    // Actualizar datasets según el tipo seleccionado
    if (this.activeReportType === 'inventario') {
      this.barChartData.datasets[0].data = datosDistribuidos;
    } else if (this.activeReportType === 'ventas') {
      this.barChartData.datasets[1].data = datosDistribuidos;
    }

    console.log('Gráfica actualizada con', cantidadRegistros, 'registros filtrados');
    
    // Forzar actualización del gráfico
    this.barChartData = { ...this.barChartData };
    this.chart?.update();
  }
  
  crearGrafica(): void {
    console.log('Creando gráfica para:', this.activeReportType, 'en período:', this.activeDateTab);
    console.log('Datos filtrados:', this.reportesFiltrados);
    
    if (this.isBrowser) {
      this.actualizarGraficaConDatos();
    }
  }
}