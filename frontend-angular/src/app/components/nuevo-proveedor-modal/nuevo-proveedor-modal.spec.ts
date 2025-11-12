import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NuevoProveedorModal } from './nuevo-proveedor-modal';

describe('NuevoProveedorModal', () => {
  let component: NuevoProveedorModal;
  let fixture: ComponentFixture<NuevoProveedorModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NuevoProveedorModal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NuevoProveedorModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
