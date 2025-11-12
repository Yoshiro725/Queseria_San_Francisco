import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NuevaVentaModal } from './nueva-venta-modal';

describe('NuevaVentaModal', () => {
  let component: NuevaVentaModal;
  let fixture: ComponentFixture<NuevaVentaModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NuevaVentaModal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NuevaVentaModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
