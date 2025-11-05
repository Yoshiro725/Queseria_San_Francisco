import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NuevaRecetaModal } from './nueva-receta-modal';

describe('NuevaRecetaModal', () => {
  let component: NuevaRecetaModal;
  let fixture: ComponentFixture<NuevaRecetaModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NuevaRecetaModal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NuevaRecetaModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
