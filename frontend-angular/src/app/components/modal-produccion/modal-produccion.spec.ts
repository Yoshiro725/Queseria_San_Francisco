import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalProduccion } from './modal-produccion';

describe('ModalProduccion', () => {
  let component: ModalProduccion;
  let fixture: ComponentFixture<ModalProduccion>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalProduccion]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ModalProduccion);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
